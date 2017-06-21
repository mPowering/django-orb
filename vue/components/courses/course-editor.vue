<script>
import CourseSection from '@/courses/course-section'
import CourseResource from '@/courses/course-resource'
import draggable from 'vuedraggable'

export default {
    name: 'course-editor',
    components: {
        draggable,
        CourseSection,
        CourseResource
    },
    props: {
        title: {
            type: String,
            default: 'New Course'
        },
        sections: {
            type: Array,
            default: () => []
        },
        labels: {
            type: Object,
            default: () => {
                return {
                    edit_title: 'Edit Course Title',
                    save_title: 'Save Course Title',
                    add_section: 'Add Course Section',
                    remove_section: 'Remove Course Section',
                    add_activity: 'Add Text Activity',
                    save: 'Save Course',
                    search: 'Search',
                    new_course_title: 'New Course'
                }
            }
        }
    },
    data () {
        return {
            course_title: this.title,
            course_sections: this.sections,
            edit_head: false,
            q: '',
            resource_api: '/api/v1/',
            available_resources: []
        }
    },
    methods: {
        editTitle () { this.edit_head = true },
        saveTitle () { this.edit_head = false },
        addSection () { this.course_sections.push([]) },
        removeSection (id) {
            this.course_sections = this.course_sections.filter(
                (section, index) => {
                    return index !== id
                }
            )
        },
        saveCourse () {
            let course = {
                title: this.course_title,
                sections: this.course_sections,
            }
            console.log(JSON.stringify(course))
            this.$http.post('.', course)
                .then(
                    (response) => console.log(response)
                )
                .catch(
                    (error) => console.error(error)
                )
        },
        searchResources () {
            console.log({
                format: 'json',
                q: this.q
            })

            this.$http.get(
                `${this.resource_api}resource/search/`,
                {
                    params: {
                        format: 'json',
                        q: this.q
                    }
                }
            )
                .then(
                    (response) => {
                        console.log(response)
                        this.available_resources = response.data.objects
                    }
                )
                .catch(
                    (error) => console.error(error)
                )
        }
    },
    beforeMount () {
        if (this.labels.new_course_title && !this.title) {
            this.course_title = this.labels.new_course_title
        }
    }
}
</script>

<template>
    <div class="course-editor">
        <header class="course-editor-hdr row">
            <template v-if="edit_head">
                <div class="input-group col-sm-6">
                    <input 
                        class="form-control" 
                        
                        v-model="course_title"
                    >
                    <span class="input-group-btn">
                        <button 
                            class="btn btn-default" 
                            v-text="labels.save_title" 
                            @click="saveTitle"
                        ></button>
                    </span>
                </div>
            </template>
            <template v-else>
                <h3 
                    class="course-editor-hed col-sm-6"
                    @click="editTitle" 
                >
                    <span v-text="course_title"></span>
                    <button 
                        class="btn btn-default btn-xs" 
                        v-text="labels.edit_title" 
                        @click="editTitle"
                    ></button>
                </h3>
            </template>
        </header>
        <div class="row">
            <div class="course-editor col-sm-9">
                <div class="list-group">
                    <draggable :list="course_sections">
                        <course-section 
                            class="list-group-item"
                            v-for="section, index in course_sections"
                            :key="section"
                            :resources="section" 
                            :labels="labels"
                        >
                            <button
                                slot="section-footer-controls"
                                class="btn btn-warning"
                                @click="removeSection(index)"
                                v-text="labels.remove_section"
                            ></button>
                        </course-section>
                    </draggable>
                </div>
                <div class="btn-group">
                    <button class="btn btn-success" v-text="labels.add_section" @click="addSection"></button>
                    <button 
                        class="btn btn-success" 
                        v-text="labels.save" 
                        @click="saveCourse"
                        :disabled="course_sections.length < 1"
                    ></button>
                </div>
            </div>
            <div class="resource-search col-sm-3">
                <div class="input-group">
                    <input 
                        class="form-control"  
                        v-model="q"
                    >
                    <span class="input-group-btn">
                        <button 
                            class="btn btn-info" 
                            @click="searchResources"
                        >Search</button>
                    </span>
                </div>
                <div class="list-group">
                    <draggable :list="available_resources" :options="{group:'resources'}">
                        <course-resource 
                            class="list-group-item"
                            v-for="resource, index in available_resources"
                            :key="resource"
                            :title="resource.title_en"
                        >
                        </course-resource>
                    </draggable>
                </div>
            </div>
        </div>
    </div>
</template>
