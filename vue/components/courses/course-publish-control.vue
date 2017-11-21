<style module src="../module.css"></style>


<template>
    <button
        class="course-publish-ctrl btn"
        :class="[$style['rhy--xStart25'], btnClass]"
        @click="commitAction"
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
            default: 'draft'
        },
        labels: {
            type: Object,
            default: () => ({
                draft: 'Publish',
                published: 'Set to Draft'
            })
        }
    },
    data () {
        return { }
    },
    methods: {
        commitAction () {
            this.$emit('toggle')
        }
    },
    computed: {
        status () { return this.courseStatus },
        isDraft () {
            return (this.status === 'draft')
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
