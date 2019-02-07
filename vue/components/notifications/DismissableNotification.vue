<script>
// Courseware currently is using JQuery with Bootstrap, so not going to reinvent wheel
//  and will let bootstrap dismissable run
export default {
    name: "DismissableNotification",
    props: {
        // @prop    active
        // @desc    is the notification active
        active: {
            type: Boolean,
            default: false
        },

        // @prop    message
        // @desc    the passed message to show
        message: {
            type: String,
            default: "General warning"
        },

        // @prop    status
        // @desc    the theme (bootstrap) to be applied
        status: {
            type: String,
            default: "info"
        }
    },
    // @lifecycle   mounted
    // @desc        when mounting the notification, run the dismiss method in 3000ms
    mounted () {
        window.setTimeout(this.dismiss, 3000)
    },
    methods: {
        // @func    dismiss
        // @desc    when manually dismissing the element, inform parent
        dismiss () { this.$emit('dismissed') }
    }
}
</script>


<template>
<transition name="fade">
    <div
        class="alert alert-dismissable module:balance iso:yEnd0"
        role="alert"
        v-if="active"
        :class="`alert-${ status }`"
    >
        <button
            class="close"
            aria-label="Close"
            type="button"
            @click="dismiss"
        >
            <span aria-hidden="true">
                &times;
            </span>
        </button>

        <p v-if="message">
            {{ message }}
        </p>
    </div>
</transition>
</template>


<style>
.fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}
</style>
