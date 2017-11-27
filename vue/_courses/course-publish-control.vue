<style module src="../module.css"></style>


<template>

    <button
        class="course-publish-ctrl btn"
        :class="[$style['rhy--xStart25'], btnClass]"
        @click="commitGenericAction"
    >
        <span
            class="glyphicon"
            :class="iconClass"
            aria-hidden="true"
        ></span>
        <span
            class="course-publish-ctrl-label"
            v-text="publishLabel"
        ></span>
    </button>

</template>


<script>
export default {
    name: 'course-publish-control',
    props: {
        courseStatus: {
            type: String,
            default: 'inactive'
        },
        labels: {
            type: Object,
            default: () => ({
                inactive: 'Publish',
                active: 'Set to Draft'
            })
        }
    },
    data () {
        return { }
    },
    methods: {
        commitGenericAction () {
            this.$emit('genericAction')
        }
    },
    computed: {
        status () { return this.courseStatus },
        isDraft () {
            return (this.status === 'inactive')
        },
        iconClass () {
            return {
                'glyphicon-cloud-upload': this.isDraft,
                'glyphicon-cloud-download': !this.isDraft
            }
        },
        btnClass () {
            return {
                'btn-primary': this.isDraft,
                'btn-default': !this.isDraft
            }
        },
        publishLabel () {
            return this.labels[this.status]
        }
    }
}
</script>
