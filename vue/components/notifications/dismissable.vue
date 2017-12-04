<style module src="../module.css"></style>


<template>
    <div
        class="alert alert-dismissable"
        :class="statusClass"
        role="alert"
    >
        <button
            type="button"
            class="close"
            aria-label="Close"
            @click="dismiss($event)"
        >
            <span aria-hidden="true">&times;</span>
        </button>
        <p v-if="message" v-text="message"></p>
    </div>
</template>


<script>
// Courseware currently is using JQuery with Bootstrap, so not going to reinvent wheel
//  and will let bootstrap dismissable run
export default {
    name: 'course-notification',
    props: {
        message: {
            type: String,
            default: 'General warning'
        },
        status: {
            type: String,
            default: 'info'
        }
    },
    data () {
        return {
            statusType: this.status
        }
    },
    methods: {
        checkStatus (statusType) {
            return (statusType === this.statusType)
        },
        dismiss ($event) {
            this.$emit('dismissed')
        }
    },
    computed: {
        statusClass () {
            return {
                'alert-success': this.checkStatus('success'),
                'alert-info': this.checkStatus('info'),
                'alert-warning': this.checkStatus('warning'),
                'alert-danger': this.checkStatus('danger'),
            }
        }
    },
    mounted () {
        window.setTimeout(this.dismiss, 3000)
    }
}
</script>
