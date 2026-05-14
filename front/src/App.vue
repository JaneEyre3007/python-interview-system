<script setup lang="ts">
import { zhCN, dateZhCN, NConfigProvider, NMessageProvider, NDialogProvider, NNotificationProvider, NLoadingBarProvider } from "naive-ui"
import type { GlobalThemeOverrides } from "naive-ui"

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#2563EB',
    primaryColorHover: '#3B82F6',
    primaryColorPressed: '#1D4ED8',
    primaryColorSuppl: '#3B82F6',
    borderRadius: '8px',
    bodyColor: '#F9FAFB',
    cardColor: '#FFFFFF',
    modalColor: '#FFFFFF',
    popoverColor: '#FFFFFF',
    tableColor: '#FFFFFF',
    inputColor: '#FFFFFF',
    actionColor: '#F3F4F6',
    tagColor: '#F3F4F6',
    hoverColor: '#F9FAFB',
    borderColor: '#E5E7EB',
    dividerColor: '#E5E7EB',
    textColorBase: '#111827',
    textColor1: '#111827',
    textColor2: '#4B5563',
    textColor3: '#9CA3AF',
    placeholderColor: '#9CA3AF',
    iconColor: '#9CA3AF',
    successColor: '#059669',
    errorColor: '#DC2626',
    warningColor: '#D97706',
    infoColor: '#2563EB',
    fontFamily: 'Inter, "Noto Sans SC", -apple-system, BlinkMacSystemFont, sans-serif',
    fontFamilyMono: '"JetBrains Mono", "Fira Code", monospace',
    fontSize: '14px',
    fontSizeSmall: '12px',
    fontSizeMini: '11px',
    fontWeight: '400',
    fontWeightStrong: '600',
  }
}
</script>

<template>
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN" :theme-overrides="themeOverrides">
    <n-loading-bar-provider>
      <n-message-provider>
        <n-notification-provider>
          <n-dialog-provider>
            <div class="h-screen w-screen">
              <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                  <component :is="Component" />
                </transition>
              </router-view>
            </div>
          </n-dialog-provider>
        </n-notification-provider>
      </n-message-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
