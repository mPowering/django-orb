<script>
// Courseware currently is using JQuery with Bootstrap, so not going to reinvent wheel
//  and will let bootstrap dismissable run
export default {
    name: "DismissableNotification",
    props: {
        active: {
            type: Boolean,
            default: false
        },
        message: {
            type: String,
            default: "General warning"
        },
        status: {
            type: String,
            default: "info"
        }
    },
    methods: {
        dismiss () { this.$emit('dismissed') }
    },
    mounted () {
        window.setTimeout(this.dismiss, 3000)
    }
}
</script>


<template>
<transition name="fade">
    <div
        class="alert alert-dismissable"
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
