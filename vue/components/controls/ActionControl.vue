<script>
export default {
    name: "ActionControl",
    props: {
        glyph: {
            type: [Boolean, String],
            default: false
        },
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
