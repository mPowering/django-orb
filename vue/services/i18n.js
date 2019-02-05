// @prop    i18n
        // @desc    data object mapping internationalizations for app
export default {
    install (Vue, options) {
        let {
            defaultTranslations,
            translations,
        } = options

        Vue.prototype.$i18n = {
            ...defaultTranslations,
            ...translations
        }
    }
}
