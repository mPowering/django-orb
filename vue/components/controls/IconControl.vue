<script>
export default {
    name: "IconControl",
    props: {
        // @prop    glyph
        // @desc    passed glyph class for a glyph icon
        // @        if none, no icon will be shown
        glyph: {
            type: [Boolean, String],
            default: false
        },
    }
}
</script>

<template functional>
<button
    class="glyph module:static flex:hAuto--p:middle--s:base rhy:xStart25"
    :class="data.staticClass"
    v-bind="data.attrs"
    v-on="listeners"
>
    <span
        class="glyphicon"
        aria-hidden="true"
        v-if="props.glyph"
        :class="`glyphicon-${ props.glyph }`"
    ></span>

    <span class="sr-only">
        <slot></slot>
    </span>
</button>
</template>
