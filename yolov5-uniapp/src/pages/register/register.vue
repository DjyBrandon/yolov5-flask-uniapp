<template>
    <view style="padding-top: 15vh" class="tn-text-4xl tn-mt tn-flex-center">
        基于深度学习的输电线路异物检测系统
    </view>
    <view class="tn-mt tn-flex-center">
        <TnForm style="padding-top: 5vh; width: 15vw" ref="formRef" :model="formData" :rules="formRules">
            <TnFormItem label="账号" prop="username">
                <TnInput v-model="formData.username"/>
            </TnFormItem>
            <TnFormItem label="密码" prop="password">
                <TnInput v-model="formData.password"/>
            </TnFormItem>
        </TnForm>
    </view>
    <view class="tn-mt tn-flex-center">
        <TnButton size="lg" @click="submitForm">注册</TnButton>
    </view>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue'
import TnForm from '@tuniao/tnui-vue3-uniapp/components/form/src/form.vue'
import TnFormItem from '@tuniao/tnui-vue3-uniapp/components/form/src/form-item.vue'
import TnButton from '@tuniao/tnui-vue3-uniapp/components/button/src/button.vue'
import TnInput from '@tuniao/tnui-vue3-uniapp/components/input/src/input.vue'

import type {FormRules, TnFormInstance} from '@tuniao/tnui-vue3-uniapp'

const formRef = ref<TnFormInstance>()

// 表单数据
const formData = reactive({
    username: 'brandon',
    password: '123',
})

// 规则
const formRules: FormRules = {
    username: [
        {required: true, message: '请输入账号', trigger: ['change', 'blur']},
        {
            pattern: /^[\w-]{4,16}$/,
            message: '请输入4-16位英文、数字、下划线、横线',
            trigger: ['change', 'blur'],
        },
    ],
    password: [
        {required: true, message: '请输入密码', trigger: ['change', 'blur']}
    ]
}

/* 提交表单 */

const baseApi = import.meta.env.VITE_APP_BASE_API

const submitForm = () => {
    formRef.value?.validate((valid: any) => {
        if (valid) {
            uni.request({
                url: baseApi + '/register',
                method: 'POST',
                data: formData,
            }).then(
                ({data}) => {
                    if (data.code == 200) {
                        tn('/pages/login/login')
                    } else {
                        uni.showToast({
                            title: data.message,
                            icon: 'none',
                        })
                    }
                }
            )
        } else {
            uni.showToast({
                title: '账号和密码是必填',
                icon: 'none',
            })
        }
    })
}

const tn = (e: string) => {
    uni.navigateTo({
        url: e,
    })
}
</script>