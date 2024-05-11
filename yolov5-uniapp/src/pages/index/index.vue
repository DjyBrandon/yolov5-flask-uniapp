<template>
    <view class="tn-w-screen tn-h-screen tn-flex-wrap tn-p">
        <view class="tn-flex-column">
            <TnButton class="tn-m-xl" size="xl" @click="detect">异物检测</TnButton>
            <TnButton class="tn-m-xl" size="xl" type="warning" @click="tn('/pages/history/history')">历史记录</TnButton>
            <TnButton class="tn-m-xl" size="xl" type="danger" @click="tn('/pages/login/login')">退出系统</TnButton>
        </view>
        <view class="tn-flex-wrap" style="flex: 1">
            <template v-for="item in detectUrl">
                <image class="tn-p-sm" style="width: 50%;" mode="widthFix" :src="item.ori"></image>
                <image class="tn-p-sm" style="width: 50%;" mode="widthFix" :src="item.det"></image>
            </template>
        </view>
    </view>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import TnButton from '@tuniao/tnui-vue3-uniapp/components/button/src/button.vue'

const baseApi = import.meta.env.VITE_APP_BASE_API
const userId = ref(0)
onMounted(() => {
    userId.value = uni.getStorageSync("userId")
})

const detectUrl = ref([]) as any
const detect = () => {
    uni.chooseImage({
        success: (chooseImageRes) => {
            const tempFilePaths = chooseImageRes.tempFilePaths;
            for (let i = 0; i < tempFilePaths.length; i++) {
                uni.uploadFile({
                    url: baseApi + '/detect',
                    filePath: tempFilePaths[i],
                    name: 'file',
                    formData: {
                        'userId': userId.value
                    },
                    success: (uploadFileRes) => {
                        const res = JSON.parse(uploadFileRes.data)
                        console.log(res)
                        detectUrl.value.push(res[0])
                        console.log(detectUrl.value)
                    }
                });
            }
        }
    });
}

const tn = (e: string) => {
    uni.navigateTo({
        url: e,
    })
}

</script>

<style lang="scss" scoped>
</style>
