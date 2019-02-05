<script>
export default {
    name: "ActionControl",
    props: {
        // @prop    glyph
        // @desc    passed glyph class for a glyph icon
        // @        if none, no icon will be shown
        glyph: {
            type: [Boolean, String],
            default: false
        },

        // @prop    theme
        // @desc    simplified prop passing of a bootstrap theme name
        theme: {
            type: String,
            default: "default"
        }
    }
}
</script>

<template functional>
<button
    class="btn module:static flex:hAuto--p:middle--s:base rhy:xStart25"
    :class="[data.staticClass, `btn-${ props.theme }`]"
    v-bind="data.attrs"
    v-on="listeners"
>
    <span
        class="glyphicon"
        aria-hidden="true"
        v-if="props.glyph"
        :class="`glyphicon-${ props.glyph }`"
    ></span>
    <slot></slot>
</button>
</template>
