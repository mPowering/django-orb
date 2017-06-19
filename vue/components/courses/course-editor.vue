<script>
import CourseSection from '@/courses/course-section'

export default {
    name: 'course-editor',
    components: {
        CourseSection
    },
    props: {
        title: String,
        sections: Array,
        labels: {
            type: Object,
            default: () => {
                return {
                    edit_title: 'Edit Course Title',
                    save_title: 'Save Course Title',
                    add_section: 'Add Course Section',
                    add_resource: 'Add Section Resource',
                    save: 'Save Course',
                    search: 'Search'
                }
            }
        }
    },
    data () {
        return {
            course_title: 'New Course',
            course_sections: [],
            edit_head: false,
            resource_api: 'http://localhost:8000/api/v1/?format=json'
        }
    },
    methods: {
        editTitle () { this.edit_head = true },
        saveTitle () { this.edit_head = false },
        addSection () { this.course_sections.push([]) },
        saveCourse () {
            let course = {
                title: this.course_title,
                sections: this.course_sections,
            }

            console.log(course)

            this.$http.post('.', course)
                .then(
                    (response) => console.log(response)
                )
                .catch(
                    (error) => console.error(error)
                )
        },
        getResource () {
            this.$http.get(this.resource_api)
                .then(
                    (response) => console.log(response)
                )
                .catch(
                    (error) => console.error(error)
                )
        }
    },
    beforeMount () {
        this.course_title = (this.title)
            ? this.title
            : this.course_title
        this.course_sections = (this.sections && this.sections instanceof Array)
            ? this.sections
            : this.course_sections
    }
}
</script>

<template>
    <div class="course-editor container-fluid">
        <div class="row">
            <div class="course-editor col-lg-4">
                <header class="course-editor-hdr">
                    <div class="input-group">
                        <template v-if="edit_head">
                            <input 
                                class="form-control" 
                                @blur="saveTitle" 
                                v-model="course_title"
                            >
                            <span class="input-group-btn">
                                <button 
                                    class="btn btn-default" 
                                    v-text="labels.save_title" 
                                    @click="saveTitle"
                                ></button>
                            </span>
                        </template>
                        <template v-else>
                            <h3 
                                @click="editTitle" 
                                class="course-editor-hed"
                                v-text="course_title"
                            ></h3>
                            <span class="input-group-btn">
                                <button 
                                    class="btn btn-default btn-xs" 
                                    v-text="labels.edit_title" 
                                    @click="editTitle"
                                ></button>
                            </span>
                        </template>
                    </div>
                </header>
                <ul class="list-group">
                    <li class="list-group-item" v-for="section in course_sections">
                        <course-section :resources="section" :labels="labels"></course-section>
                    </li>
                </ul>
                <button class="btn btn-default" v-text="labels.add_section" @click="addSection"></button>
                <button class="btn btn-default" v-text="labels.save" @click="saveCourse"></button>
                <button class="btn btn-default" v-text="labels.search" @click="getResource"></button>
            </div>
        </div>
    </div>
</template>
