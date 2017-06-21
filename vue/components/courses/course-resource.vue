<script>
export default {
    name: 'course-resource',
    props: {
        title: String,
        labels: {
            type: Object,
            default: () => {
                return {
                    edit_resource: 'Edit Section Resource',
                    save_resource: 'Save Section Resource'
                }
            }
        }
    },
    data () {
        return {
            resource_title: 'Unnamed Resource',
            resource_description: '',
            edittable: false
        }
    },
    methods: {
        editResource () {
            this.edittable = !this.edittable
        },
        updateResource () {
            this.$emit('update:title', this.resource_title)
            this.editResource()
        }
    },
    beforeMount () {
        this.resource_title = (this.title)
            ? this.title
            : this.resource_title
    }
}
</script>

<template>
  <div class="course-resource">
    <template v-if="edittable">
        <input class="form-control" v-model="resource_title">
        <textarea class="form-control" v-model="resource_description">
        </textarea>
        <button class="btn btn-success" type="button" @click="updateResource">Save</button>
    </template>
    <template v-else>
        <h5 v-text="resource_title"></h5>
        <div v-text="resource_description"></div>
        <button class="btn btn-primary" type="button" @click="editResource">Edit</button>
        <slot name="resource-footer-controls"></slot>
    </template>
    
  </div>
</template>

