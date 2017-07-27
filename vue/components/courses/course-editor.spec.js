import Vue from 'vue'
import Axios from 'axios'

import { mount } from 'avoriaz'
import MockAdapter from 'axios-mock-adapter'

import CourseEditor from './course-editor.vue'
import CourseSection from './course-section.vue'

const moxios = new MockAdapter(Axios)

let ORBLabels = {
    edit_title: "Edit Course Title",
    save_title: "Save Course Title",
    add_section: 'Add Course Section',
    remove_section: 'Remove Course Section',
    add_activity: 'Add Text Activity',
    create: 'Create Course',
    save: 'Save Course',
    search: 'Search',
    new_course_title: 'New Course'
}

describe('CourseEditor', () => {
    let wrapper
    let defaultProps = {
        title: "New Course",
        sections:  [{ resources: []}],
        labels: ORBLabels
    }


    function loader (
        propsD = {
            title: "New Course",
            sections:  [{ resources: []}],
            labels: ORBLabels
        }
    ) {
        let propsData = Object.assign({}, propsD)
        wrapper = mount(CourseEditor, { propsData, attachToDocument: true })
    }

    describe("Initial Setup: ", () => {
        beforeEach(() => {
            loader()        
        })
        
        it('should be in the script', () => {
            expect(CourseEditor.name).toEqual('course-editor')
        })

        it('should mount', () => {
            expect(wrapper.is(".course-editor")).toBe(true)
        })  

        it('has a BeforeMount Hook', () => {
            expect(typeof CourseEditor.created).toBe('function')
        })
    })

    describe("Course Title", () => {
        beforeEach(() => {
            loader()        
        })

        it('can be passed as a property', () => {
            expect(CourseEditor.props.title).toBeDefined()
        })
    
        describe("title is loaded", () => {

            describe("no title is given", () => {
                beforeEach(() => {
                    loader({ })
                })

                it("loads the default title", () => {
                    expect(wrapper.vm.$props.title).toEqual(defaultProps.title)
                    expect(wrapper.data().course_title).toEqual(defaultProps.title)
                })

                it("loads default title on the element", () => {
                    let header = wrapper.find(".course-editor-hed > span")[0]
                    expect(header.text()).toEqual(defaultProps.title)
                    expect(header.text()).toEqual(defaultProps.labels.new_course_title)
                })
            })

            describe("title is initially blank", () => {
                beforeEach(() => {
                    loader({ title: ""})
                })

                it("loads empty", () => {
                    expect(wrapper.vm.$props.title).toEqual('')
                    expect(wrapper.vm.title).toEqual('')
                    expect(wrapper.vm.course_title).toEqual(defaultProps.title)
                })
            
                it("loads default title on the element", () => {
                    let header = wrapper.find(".course-editor-hed > span")[0]
                    expect(header.text()).toEqual(defaultProps.title)
                    expect(header.text()).toEqual(defaultProps.labels.new_course_title)
                })
            })

            describe("title is initially given", () => {
                let title = "Test Title"
                beforeEach(() => {
                    loader({ title })
                })
            
                it("loads as prop", () => {
                    expect(wrapper.vm.$props.title).toEqual(title)
                    expect(wrapper.vm.title).toEqual(title)
                    expect(wrapper.data().course_title).toEqual(title)
                })

                it("loads the title on the element", () => {
                    let header = wrapper.find(".course-editor-hed > span")[0]
                    expect(header.text()).toEqual(title)
                })
            })

            it("can be edited", () => {
                expect(wrapper.vm.edit_head).toBe(false)
                wrapper.vm.editTitle()
                wrapper.vm.course_title = "Test"
                expect(wrapper.vm.edit_head).toBe(true)
                expect(wrapper.vm.course_title).toEqual("Test")
            })
            
            it("editing feature can be activated/deactivated", () => {
                expect(wrapper.vm.edit_head).toBe(false)
                
                let edit_btn = wrapper.find(".course-editor-hed-edit")[0]
                edit_btn.trigger('click')
                
                let title_input = wrapper.find(".course-editor-hdr .form-control")[0]
                let save_btn = wrapper.find(".course-editor-hed-save")[0]
                edit_btn = wrapper.find(".course-editor-hed-edit")[0]
                
                expect(wrapper.vm.edit_head).toBe(true)
                expect(title_input).toBeDefined()
                expect(save_btn).toBeDefined()
                expect(edit_btn).toBeUndefined()

                save_btn.trigger("click")
                edit_btn = wrapper.find(".course-editor-hed-edit")[0]
                save_btn = wrapper.find(".course-editor-hed-save")[0]
                let title_hed = wrapper.find(".course-editor-hed span")[0]

                expect(wrapper.vm.edit_head).toBe(false)
                expect(title_hed).toBeDefined()
                expect(edit_btn).toBeDefined()
                expect(save_btn).toBeUndefined()
            })

        })
    
    })

    describe("Course Sections", () => {
        it('is a property', () => {
            expect(CourseEditor.props.sections).toBeDefined()
        })

        describe("sections is/are loaded", () => {
            describe("no sections are given", () => {
                beforeEach(() => {
                    loader({ })
                })

                it("loads the default sections", () => {
                    expect(wrapper.vm.$props.sections).toEqual( defaultProps.sections )
                    expect(wrapper.vm.sections).toEqual( defaultProps.sections )
                    expect(wrapper.vm.course_sections).toEqual(defaultProps.sections)
                    expect(wrapper.vm.course_sections.length).toEqual(1)
                    expect(wrapper.vm.course_sections instanceof Array).toBe(true)
                    
                })
                
                it("loads default section in the template", () => {
                    expect(wrapper.contains(CourseSection)).toBe(true)
                })
            })
        })

        describe("sections are initially blank", () => {
            beforeEach(() => {
                loader({ sections: [] })
            })

            it("still loads default sections", () => {
                expect(wrapper.vm.$props.sections).toEqual( [] )
                expect(wrapper.vm.course_sections).toEqual( defaultProps.sections )
                expect(wrapper.vm.course_sections.length).toEqual(1)
            })
            
            it("loads default section in the template", () => {
                expect(wrapper.contains(CourseSection)).toBe(true)
            })
        })

        describe("sections are initially given", () => {
            let sections = [{resources: []}, {resources: []}]
            
            beforeEach(() =>{
                loader({ sections })
            })

            it("loads as a prop", () => {
                expect(wrapper.vm.$props.sections).toEqual(sections)
                expect(wrapper.vm.course_sections).toEqual(sections)
                expect(wrapper.vm.course_sections.length).toEqual(2)
            })

            it("loads sections into template", () => {
                expect(wrapper.contains(CourseSection)).toBe(true)
                expect(wrapper.find(CourseSection).length).toEqual(2)
            })
        })

        describe("Adding Sections", () => {
            beforeEach(() =>{
                loader()
            })
            
            it("adds a section", () => {
                expect(wrapper.vm.course_sections.length).toEqual(1)
                wrapper.vm.addSection()
                wrapper.vm.addSection()
                expect(wrapper.vm.course_sections.length).toEqual(3)
            })

            it("adds a section via the ui", () => {
                expect(wrapper.vm.course_sections.length).toEqual(1)
                let add_ctrl = wrapper.find(".course-sections-add")[0]
                add_ctrl.trigger("click")
                expect(wrapper.vm.course_sections.length).toEqual(2)
            })
        })

        describe("Subtracting Sections", () => {
            beforeEach(() =>{
                loader()
            })
        
            
            it("removes a section", () => {
                expect(wrapper.vm.course_sections.length).toEqual(1)
                wrapper.vm.removeSection(0)
                expect(wrapper.data().course_sections.length).toEqual(0)
            })

            it("removes a specific section", () => {
                expect(wrapper.vm.course_sections.length).toEqual(1)
                wrapper.vm.addSection()
                wrapper.vm.addSection()
                wrapper.vm.addSection()
                wrapper.vm.removeSection(3)
                expect(wrapper.data().course_sections.length).toEqual(3)
            })
        })
    })

    describe("Save a Course", () => {
        beforeEach(() => {
            let dProps = Object.assign({}, defaultProps)
            dProps = Object.assign(dProps, { id: 1, action: "update"})
            loader(dProps)
            wrapper.vm.$http = Axios
            moxios.onPost("/courses/1/").reply(200, {'status': 'ok', 'course_id': 1})
        })

        it("should save to db, and return an id", () => {
            expect(wrapper.vm.course_id).toEqual(1)
            expect(wrapper.vm.action).toEqual('update')
            expect(wrapper.vm.savepoint).toEqual('/courses/1/')
            
            wrapper.vm.saveCourse().then(
                () => {
                    expect(wrapper.vm.course_id).toEqual(1)
                }
            )   
        })   
    })

    describe("Create a Course", () => {
        beforeEach(() => {

            let dProps = Object.assign({}, defaultProps)
            dProps = Object.assign(dProps, { action: "create"})
            loader(dProps)
            wrapper.vm.$http = Axios
            moxios.onPost(".").reply(200, {'status': 'ok', 'course_id': 1})
        })

        it("should save to db, and return an id", () => {
            expect(wrapper.vm.course_id).toBe(false)
            expect(wrapper.vm.action).toEqual('create')
            
            
            wrapper.vm.saveCourse().then(
                () => {
                    expect(wrapper.vm.course_id).toEqual(1)
                }
            )   
        })   
        
        it("after saving, should change its save_action to 'update'", () => {
            expect(wrapper.vm.save_action).toEqual('create')
           
            wrapper.vm.saveCourse().then(
                () => {
                    expect(wrapper.vm.save_action).toEqual('update')
                }
            )
        })

        it("after saving, should change its savepoint to the updatepoint", () => {
            expect(wrapper.vm.savepoint).toEqual('.')
            
            wrapper.vm.saveCourse().then(
                () => {
                    expect(wrapper.vm.savepoint).toEqual('/courses/1/')
                }
            )
        })

        it("after saving, should change its save button label to reflect we are saving", () => {
            expect(wrapper.find(".course-save-ctrl-label")[0].text()).toEqual(ORBLabels.create)
            
            wrapper.vm.saveCourse().then(
                () => {
                    expect(wrapper.find(".course-save-ctrl-label")[0].text()).toEqual(ORBLabels.save)
                }
            )
        })
    })
})
