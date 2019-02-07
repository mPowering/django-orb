<script>
export default {
    name: "RouterControl",
    props: {
        // @prop    glyph
        // @desc    passed glyph class for a glyph icon
        // @        if none, no icon will be shown
        glyph: {
            type: [Boolean, String],
            default: false
        },

        // @prop    link
        // @desc    url to use through VueRouter
        link: {
            type: Object,
            required: true
        },

        // @prop    theme
        // @desc    simplified prop passing of a bootstrap theme name
        theme: {
            type: String,
            default: "default"
        },


    }
}
</script>

<template functional>
<router-link
    class="btn module:static flex:hAuto--p:middle--s:base rhy:xStart25"
    :class="[data.staticClass, `btn-${ props.theme }`]"
    v-bind="data.attrs"
    :to="props.link"
>
    <span
        class="glyphicon"
        aria-hidden="true"
        v-if="props.glyph"
        :class="`glyphicon-${ props.glyph }`"
    ></span>
    <slot></slot>
</router-link>
</template>
