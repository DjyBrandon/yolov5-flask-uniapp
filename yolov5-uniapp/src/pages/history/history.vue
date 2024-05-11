<template>
    <view style="height: 15vh" class="tn-text-bold tn-text-4xl tn-flex-center-center">
        历史记录
    </view>
    <view class="tn-flex-wrap tn-flex-center-center">
        <image class="tn-m" v-for="item in historyUrl" :src="`data:image/jpg;base64,${item}`"></image>
    </view>
</template>

<script setup lang="ts">
import {onMounted, ref, toRaw} from 'vue'

const baseApi = import.meta.env.VITE_APP_BASE_API
const userId = uni.getStorageSync("userId")

onMounted(() => {
    history()
})

const historyUrl = ref({})

const history = () => {
    uni.request({
        url: baseApi + '/history',
        method: 'GET',
        data: {
            "userId": userId
        },
    }).then(
        ({data}) => {
            const res = ref({})
            res.value = data
            historyUrl.value = toRaw(res.value)
        }
    )
}

</script>

<style lang="scss" scoped>
.image-data {
    width: calc(100% - 20px);
    margin: 10px;

    .image {
        width: 100%;
        height: auto;
    }
}
</style>
