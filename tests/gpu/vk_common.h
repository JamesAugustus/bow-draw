// vk_common.h -- small Vulkan helper (instance, buffers, pipelines, timestamps). SPDX-License-Identifier: MIT
// Identifiers are in Turkish: tampon = buffer, boru = pipeline, yukle/indir = upload/download, damga = timestamp.
// Compute buffers live in VRAM (DEVICE_LOCAL); upload and download go through a HOST_CACHED staging buffer with vkCmdCopyBuffer.
// With the environment variable FX_STATS=1 the driver statistics of every pipeline (registers, instruction count, wave size) are printed.
#ifndef VK_COMMON_H
#define VK_COMMON_H
#include <vulkan/vulkan.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define CK(x) do { VkResult _r = (x); if (_r != VK_SUCCESS) { fprintf(stderr, "vulkan error %d at line %d\n", _r, __LINE__); exit(1); } } while (0)
static double simdi(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

typedef struct { VkBuffer b; VkDeviceMemory m; void *p; VkDeviceSize sz; } Tampon;
static VkInstance vk_inst; static VkPhysicalDevice vk_pd; static VkDevice vk_dev; static VkQueue vk_q; static uint32_t vk_qi;
static VkCommandPool vk_cp; static VkPhysicalDeviceProperties vk_pr; static int vk_istat = 0; static int vk_int64 = 0;
static VkQueryPool vk_qp;

static uint32_t vk_bellek_turu(uint32_t bits, VkMemoryPropertyFlags f) {
    VkPhysicalDeviceMemoryProperties mp; vkGetPhysicalDeviceMemoryProperties(vk_pd, &mp);
    for (uint32_t i = 0; i < mp.memoryTypeCount; i++) if ((bits & (1u << i)) && (mp.memoryTypes[i].propertyFlags & f) == f) return i;
    return UINT32_MAX;
}

static void vk_baslat(void) {
    VkApplicationInfo app = { VK_STRUCTURE_TYPE_APPLICATION_INFO }; app.apiVersion = VK_API_VERSION_1_2;
    VkInstanceCreateInfo ii = { VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO }; ii.pApplicationInfo = &app;
    CK(vkCreateInstance(&ii, NULL, &vk_inst));
    uint32_t n = 8; VkPhysicalDevice pds[8]; vkEnumeratePhysicalDevices(vk_inst, &n, pds); if (!n) { fprintf(stderr, "no graphics card found\n"); exit(1); }
    vk_pd = pds[0];
    for (uint32_t i = 0; i < n; i++) { vkGetPhysicalDeviceProperties(pds[i], &vk_pr); if (vk_pr.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) { vk_pd = pds[i]; break; } }
    vkGetPhysicalDeviceProperties(vk_pd, &vk_pr);
    uint32_t qn = 16; VkQueueFamilyProperties qf[16]; vkGetPhysicalDeviceQueueFamilyProperties(vk_pd, &qn, qf);
    vk_qi = 0; for (uint32_t i = 0; i < qn; i++) if (qf[i].queueFlags & VK_QUEUE_COMPUTE_BIT) { vk_qi = i; break; }
    float pri = 1; VkDeviceQueueCreateInfo qc = { VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO }; qc.queueFamilyIndex = vk_qi; qc.queueCount = 1; qc.pQueuePriorities = &pri;
    VkPhysicalDeviceFeatures2 f2 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2 };
    VkPhysicalDeviceVulkan12Features f12 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_2_FEATURES };
    VkPhysicalDevicePipelineExecutablePropertiesFeaturesKHR fpe = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PIPELINE_EXECUTABLE_PROPERTIES_FEATURES_KHR };
    f2.pNext = &f12; f12.pNext = &fpe;
    vkGetPhysicalDeviceFeatures2(vk_pd, &f2);
    vk_int64 = f2.features.shaderInt64;
    VkPhysicalDeviceFeatures2 e2 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2 };
    VkPhysicalDeviceVulkan12Features e12 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_2_FEATURES };
    VkPhysicalDevicePipelineExecutablePropertiesFeaturesKHR epe = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PIPELINE_EXECUTABLE_PROPERTIES_FEATURES_KHR };
    e2.features.shaderInt64 = f2.features.shaderInt64;
    e12.hostQueryReset = f12.hostQueryReset;
    const char *uz[2]; uint32_t nuz = 0;
    const char *ist = getenv("FX_STATS");
    if (ist && ist[0] == '1' && fpe.pipelineExecutableInfo) { vk_istat = 1; epe.pipelineExecutableInfo = VK_TRUE; uz[nuz++] = VK_KHR_PIPELINE_EXECUTABLE_PROPERTIES_EXTENSION_NAME; e12.pNext = &epe; }
    e2.pNext = &e12;
    VkDeviceCreateInfo di = { VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO }; di.queueCreateInfoCount = 1; di.pQueueCreateInfos = &qc;
    di.pNext = &e2; di.enabledExtensionCount = nuz; di.ppEnabledExtensionNames = uz;
    CK(vkCreateDevice(vk_pd, &di, NULL, &vk_dev)); vkGetDeviceQueue(vk_dev, vk_qi, 0, &vk_q);
    VkCommandPoolCreateInfo cpo = { VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO }; cpo.queueFamilyIndex = vk_qi; cpo.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
    CK(vkCreateCommandPool(vk_dev, &cpo, NULL, &vk_cp));
    VkQueryPoolCreateInfo qpi = { VK_STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO }; qpi.queryType = VK_QUERY_TYPE_TIMESTAMP; qpi.queryCount = 2;
    CK(vkCreateQueryPool(vk_dev, &qpi, NULL, &vk_qp));
    fprintf(stderr, "card: %s ; shaderInt64=%d\n", vk_pr.deviceName, vk_int64);
}

// vram=1: DEVICE_LOCAL (not mapped). vram=0: HOST_CACHED (mapped from the CPU, staging buffer).
static Tampon vk_tampon(VkDeviceSize sz, int vram) {
    Tampon t; memset(&t, 0, sizeof t); t.sz = sz;
    VkBufferCreateInfo bi = { VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO }; bi.size = sz;
    bi.usage = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_SRC_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT;
    CK(vkCreateBuffer(vk_dev, &bi, NULL, &t.b));
    VkMemoryRequirements mr; vkGetBufferMemoryRequirements(vk_dev, t.b, &mr);
    VkMemoryAllocateInfo ai = { VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO }; ai.allocationSize = mr.size;
    if (vram) ai.memoryTypeIndex = vk_bellek_turu(mr.memoryTypeBits, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
    else {
        ai.memoryTypeIndex = vk_bellek_turu(mr.memoryTypeBits, VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT | VK_MEMORY_PROPERTY_HOST_CACHED_BIT);
        if (ai.memoryTypeIndex == UINT32_MAX) ai.memoryTypeIndex = vk_bellek_turu(mr.memoryTypeBits, VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT);
    }
    if (ai.memoryTypeIndex == UINT32_MAX) { fprintf(stderr, "no suitable memory type\n"); exit(1); }
    CK(vkAllocateMemory(vk_dev, &ai, NULL, &t.m)); CK(vkBindBufferMemory(vk_dev, t.b, t.m, 0));
    if (!vram) CK(vkMapMemory(vk_dev, t.m, 0, sz, 0, &t.p));
    return t;
}
static void vk_birak(Tampon *t) { if (t->p) vkUnmapMemory(vk_dev, t->m); vkDestroyBuffer(vk_dev, t->b, NULL); vkFreeMemory(vk_dev, t->m, NULL); memset(t, 0, sizeof *t); }

static VkCommandBuffer vk_kb_ac(void) {
    VkCommandBufferAllocateInfo cai = { VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO }; cai.commandPool = vk_cp; cai.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY; cai.commandBufferCount = 1;
    VkCommandBuffer cb; CK(vkAllocateCommandBuffers(vk_dev, &cai, &cb));
    VkCommandBufferBeginInfo bg = { VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO }; CK(vkBeginCommandBuffer(cb, &bg));
    return cb;
}
// submit and wait; returns the wall-clock time (vkQueueSubmit .. vkQueueWaitIdle)
static void vk_kb_bitir(VkCommandBuffer cb) { CK(vkEndCommandBuffer(cb)); }
static double vk_kb_gonder(VkCommandBuffer cb) {
    VkSubmitInfo si = { VK_STRUCTURE_TYPE_SUBMIT_INFO }; si.commandBufferCount = 1; si.pCommandBuffers = &cb;
    double t0 = simdi(); CK(vkQueueSubmit(vk_q, 1, &si, VK_NULL_HANDLE)); CK(vkQueueWaitIdle(vk_q)); double t1 = simdi();
    return t1 - t0;
}
static void vk_kb_birak(VkCommandBuffer cb) { vkFreeCommandBuffers(vk_dev, vk_cp, 1, &cb); }
static void vk_bariyer(VkCommandBuffer cb) {
    VkMemoryBarrier mb = { VK_STRUCTURE_TYPE_MEMORY_BARRIER };
    mb.srcAccessMask = VK_ACCESS_SHADER_WRITE_BIT | VK_ACCESS_TRANSFER_WRITE_BIT; mb.dstAccessMask = VK_ACCESS_SHADER_READ_BIT | VK_ACCESS_SHADER_WRITE_BIT | VK_ACCESS_TRANSFER_READ_BIT;
    vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT | VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT | VK_PIPELINE_STAGE_TRANSFER_BIT, 0, 1, &mb, 0, NULL, 0, NULL);
}
// write CPU data into a VRAM buffer (through the staging buffer); returns the time
static double vk_yukle(Tampon *dst, const void *src, VkDeviceSize sz) {
    double t0 = simdi(); Tampon s = vk_tampon(sz, 0); memcpy(s.p, src, sz);
    VkCommandBuffer cb = vk_kb_ac(); VkBufferCopy bc = { 0, 0, sz }; vkCmdCopyBuffer(cb, s.b, dst->b, 1, &bc); vk_kb_bitir(cb); vk_kb_gonder(cb); vk_kb_birak(cb);
    vk_birak(&s); return simdi() - t0;
}
static double vk_indir(void *dst, Tampon *src, VkDeviceSize sz) {
    double t0 = simdi(); Tampon s = vk_tampon(sz, 0);
    VkCommandBuffer cb = vk_kb_ac(); VkBufferCopy bc = { 0, 0, sz }; vkCmdCopyBuffer(cb, src->b, s.b, 1, &bc); vk_kb_bitir(cb); vk_kb_gonder(cb); vk_kb_birak(cb);
    memcpy(dst, s.p, sz); vk_birak(&s); return simdi() - t0;
}
// timestamps 0 and 1 inside the command buffer; the read returns the difference in ns
static void vk_damga_sifirla(VkCommandBuffer cb) { vkCmdResetQueryPool(cb, vk_qp, 0, 2); }
static void vk_damga(VkCommandBuffer cb, uint32_t i) { vkCmdWriteTimestamp(cb, i == 0 ? VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT : VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT, vk_qp, i); }
static double vk_damga_sure(void) {
    uint64_t ts[2]; CK(vkGetQueryPoolResults(vk_dev, vk_qp, 0, 2, sizeof ts, ts, 8, VK_QUERY_RESULT_64_BIT | VK_QUERY_RESULT_WAIT_BIT));
    return (double)(ts[1] - ts[0]) * vk_pr.limits.timestampPeriod * 1e-9;
}

typedef struct { VkPipeline pipe; VkPipelineLayout pl; VkDescriptorSetLayout dsl; VkDescriptorPool dp; VkDescriptorSet ds; uint32_t pcb; } Boru;
static void *vk_dosya(const char *ad, size_t *n) {
    FILE *f = fopen(ad, "rb"); if (!f) { perror(ad); exit(1); }
    fseek(f, 0, SEEK_END); long sl = ftell(f); fseek(f, 0, SEEK_SET); void *p = malloc(sl ? sl : 1);
    if (fread(p, 1, sl, f) != (size_t)sl) { fprintf(stderr, "cannot read %s\n", ad); exit(1); } fclose(f); *n = sl; return p;
}
static void vk_istat_bas(VkPipeline pipe, const char *ad) {
    PFN_vkGetPipelineExecutablePropertiesKHR gp = (PFN_vkGetPipelineExecutablePropertiesKHR)vkGetDeviceProcAddr(vk_dev, "vkGetPipelineExecutablePropertiesKHR");
    PFN_vkGetPipelineExecutableStatisticsKHR gs = (PFN_vkGetPipelineExecutableStatisticsKHR)vkGetDeviceProcAddr(vk_dev, "vkGetPipelineExecutableStatisticsKHR");
    if (!gp || !gs) return;
    VkPipelineInfoKHR pi = { VK_STRUCTURE_TYPE_PIPELINE_INFO_KHR }; pi.pipeline = pipe;
    uint32_t ne = 0; gp(vk_dev, &pi, &ne, NULL); VkPipelineExecutablePropertiesKHR ep[4]; if (ne > 4) ne = 4;
    for (uint32_t i = 0; i < ne; i++) { ep[i].sType = VK_STRUCTURE_TYPE_PIPELINE_EXECUTABLE_PROPERTIES_KHR; ep[i].pNext = NULL; }
    gp(vk_dev, &pi, &ne, ep);
    for (uint32_t e = 0; e < ne; e++) {
        VkPipelineExecutableInfoKHR ei = { VK_STRUCTURE_TYPE_PIPELINE_EXECUTABLE_INFO_KHR }; ei.pipeline = pipe; ei.executableIndex = e;
        uint32_t ns = 0; gs(vk_dev, &ei, &ns, NULL); VkPipelineExecutableStatisticKHR st[64]; if (ns > 64) ns = 64;
        for (uint32_t i = 0; i < ns; i++) { st[i].sType = VK_STRUCTURE_TYPE_PIPELINE_EXECUTABLE_STATISTIC_KHR; st[i].pNext = NULL; }
        gs(vk_dev, &ei, &ns, st);
        fprintf(stderr, "STATS %s wave=%u", ad, ep[e].subgroupSize);
        for (uint32_t i = 0; i < ns; i++) {
            if (st[i].format == VK_PIPELINE_EXECUTABLE_STATISTIC_FORMAT_UINT64_KHR) fprintf(stderr, " %s=%llu", st[i].name, (unsigned long long)st[i].value.u64);
        }
        fprintf(stderr, "\n");
    }
}
#include <unistd.h>
static Boru vk_boru(const char *spv_ad, uint32_t nbag, Tampon **bag, uint32_t pcb) {
    Boru B; memset(&B, 0, sizeof B); B.pcb = pcb;
    char yol[4096]; ssize_t yl = readlink("/proc/self/exe", yol, sizeof yol - 256); if (yl < 0) yl = 0; yol[yl] = 0;
    char *bol = strrchr(yol, '/'); if (bol) bol[1] = 0; else yol[0] = 0; strcat(yol, spv_ad);   // the .spv file sits next to the running program
    size_t sl; uint32_t *spv = vk_dosya(yol, &sl);
    VkDescriptorSetLayoutBinding lb[8];
    for (uint32_t i = 0; i < nbag; i++) { lb[i].binding = i; lb[i].descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER; lb[i].descriptorCount = 1; lb[i].stageFlags = VK_SHADER_STAGE_COMPUTE_BIT; lb[i].pImmutableSamplers = NULL; }
    VkDescriptorSetLayoutCreateInfo li = { VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO }; li.bindingCount = nbag; li.pBindings = lb;
    CK(vkCreateDescriptorSetLayout(vk_dev, &li, NULL, &B.dsl));
    VkPushConstantRange pcr = { VK_SHADER_STAGE_COMPUTE_BIT, 0, pcb };
    VkPipelineLayoutCreateInfo pli = { VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO }; pli.setLayoutCount = 1; pli.pSetLayouts = &B.dsl; pli.pushConstantRangeCount = pcb ? 1 : 0; pli.pPushConstantRanges = &pcr;
    CK(vkCreatePipelineLayout(vk_dev, &pli, NULL, &B.pl));
    VkShaderModuleCreateInfo smi = { VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO }; smi.codeSize = sl; smi.pCode = spv;
    VkShaderModule sm; CK(vkCreateShaderModule(vk_dev, &smi, NULL, &sm));
    VkComputePipelineCreateInfo cpi = { VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO };
    cpi.stage.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO; cpi.stage.stage = VK_SHADER_STAGE_COMPUTE_BIT; cpi.stage.module = sm; cpi.stage.pName = "main"; cpi.layout = B.pl;
    if (vk_istat) cpi.flags = VK_PIPELINE_CREATE_CAPTURE_STATISTICS_BIT_KHR;
    CK(vkCreateComputePipelines(vk_dev, VK_NULL_HANDLE, 1, &cpi, NULL, &B.pipe));
    if (vk_istat) vk_istat_bas(B.pipe, spv_ad);
    vkDestroyShaderModule(vk_dev, sm, NULL); free(spv);
    VkDescriptorPoolSize ps = { VK_DESCRIPTOR_TYPE_STORAGE_BUFFER, nbag };
    VkDescriptorPoolCreateInfo dpi = { VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO }; dpi.maxSets = 1; dpi.poolSizeCount = 1; dpi.pPoolSizes = &ps;
    CK(vkCreateDescriptorPool(vk_dev, &dpi, NULL, &B.dp));
    VkDescriptorSetAllocateInfo dai = { VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO }; dai.descriptorPool = B.dp; dai.descriptorSetCount = 1; dai.pSetLayouts = &B.dsl;
    CK(vkAllocateDescriptorSets(vk_dev, &dai, &B.ds));
    VkDescriptorBufferInfo bi[8]; VkWriteDescriptorSet wr[8]; memset(wr, 0, sizeof wr);
    for (uint32_t i = 0; i < nbag; i++) {
        bi[i].buffer = bag[i]->b; bi[i].offset = 0; bi[i].range = VK_WHOLE_SIZE;
        wr[i].sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET; wr[i].dstSet = B.ds; wr[i].dstBinding = i; wr[i].descriptorCount = 1; wr[i].descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER; wr[i].pBufferInfo = &bi[i];
    }
    vkUpdateDescriptorSets(vk_dev, nbag, wr, 0, NULL);
    return B;
}
static void vk_boru_bagla(VkCommandBuffer cb, Boru *B) {
    vkCmdBindPipeline(cb, VK_PIPELINE_BIND_POINT_COMPUTE, B->pipe);
    vkCmdBindDescriptorSets(cb, VK_PIPELINE_BIND_POINT_COMPUTE, B->pl, 0, 1, &B->ds, 0, NULL);
}
static void vk_itme(VkCommandBuffer cb, Boru *B, const void *pc) { vkCmdPushConstants(cb, B->pl, VK_SHADER_STAGE_COMPUTE_BIT, 0, B->pcb, pc); }
// split the total number of workgroups into x (at most 65535) and y; returns the x step
static uint32_t vk_dagit(VkCommandBuffer cb, uint64_t grup) {
    uint32_t gx = grup > 65535 ? 65535 : (uint32_t)grup; if (!gx) gx = 1;
    uint32_t gy = (uint32_t)((grup + gx - 1) / gx);
    vkCmdDispatch(cb, gx, gy, 1); return gx;
}
static int kiyas_d(const void *a, const void *b) { double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y); }
static double ortanca(double *v, int n) { double *c = malloc(n * sizeof *c); memcpy(c, v, n * sizeof *c); qsort(c, n, sizeof *c, kiyas_d); double m = (n & 1) ? c[n / 2] : 0.5 * (c[n / 2 - 1] + c[n / 2]); free(c); return m; }
static double enaz(double *v, int n) { double m = v[0]; for (int i = 1; i < n; i++) if (v[i] < m) m = v[i]; return m; }
#endif
