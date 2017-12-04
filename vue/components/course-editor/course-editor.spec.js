import VueTestUtils, { mount, shallow } from 'vue-test-utils'

import Axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
const moxios = new MockAdapter(Axios)

import CourseEditor from '@cmp/course-editor/course-editor'
import CourseSection from '@cmp/course-section/course-section'
import CourseNotification from '@cmp/notifications/dismissable'
import PublishControl from '@cmp/course-publish-control/course-publish-control'


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

let wrapper = {}
let vm = {}
let defaultProps = {
    title: 'New Course',
    status: 'draft',
    // sections: [{ resources: []}], -> this doesn't get deep cloned
    labels: ORBLabels
}

describe('Course Editor', () => {

    function loader (
        pData = defaultProps
    ){
        let propsData = Object.assign(
            {
                sections: [{resources: []}]
            },
            pData
        )
        wrapper = shallow(CourseEditor,
            {
                propsData
            }
        )
        // jsDom can't 'navigate' the window, so we stub the redirection
        // and just do a logic check
        wrapper.setMethods({
            redirectOnCreate () {
                const logicCheck = !!(this.initialCourseView && this.course_id)
                this.redirectLogicCheck = logicCheck
            }
        })
        vm = wrapper.vm

        vm.$http = Axios
        moxios
            .onPost("/courses/1/")
            .reply(
                200,
                {
                    'status': 'draft',
                    'course_id': 1,
                    'message': 'Your changes have been saved.'
                }
            )
        moxios
            .onPost(".")
            .reply(
                200,
                {
                    'status': 'draft',
                    'course_id': 1,
                    'message': 'Your changes have been saved.'
                }
            )
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

        it('should mount with props', () => {
            expect(wrapper.hasProp("title", "New Course")).toBe(true)
            expect(wrapper.hasProp("status", "draft")).toBe(true)
            expect(vm.sections).toEqual([{resources: []}])
            expect(vm.labels).toEqual(defaultProps.labels)
        })
    })


    describe("Course Title", () => {
        beforeEach(() => {
            loader()
        })

        it('can be passed as a property', () => {
            expect(CourseEditor.props.title).toBeDefined()
        })

        it("can be edited", () => {
            // error raises due to vue-test-utils
            expect(vm.edit_head).toBe(false)
            wrapper.find('.course-editor-hed-edit').trigger('click')
            vm.editTitle()
            wrapper.setData({ course_title: 'Test' })
            expect(vm.edit_head).toBe(true)
        })

        it("editing feature can be activated/deactivated", () => {
            expect(vm.edit_head).toBe(false)

            wrapper.find(".course-editor-hed-edit").trigger('click')

            expect(vm.edit_head).toBe(true)
            expect(
                wrapper.find(".course-editor-hdr .form-control").exists()
            ).toBe(true)
            expect(
                wrapper.find(".course-editor-hed-save").exists()
            ).toBe(true)
            expect(
                wrapper.find(".course-editor-hed-edit").exists()
            ).toBe(false)

            wrapper.find(".course-editor-hed-save").trigger('click')

            expect(vm.edit_head).toBe(false)
            expect(
                wrapper.find(".course-editor-hed-edit").exists()
            ).toBe(true)
            expect(
                wrapper.find(".course-editor-hed span").exists()
            ).toBe(true)
            expect(
                wrapper.find(".course-editor-hed-save").exists()
            ).toBe(false)
        })

        describe("title is loaded", () => {
            beforeEach(() => {
                loader({ })
            })

            it("loads the default title", () => {
                expect(wrapper.hasProp('title', defaultProps.title)).toBe(true)
                expect(vm.course_title).toEqual(defaultProps.title)
            })

            it("loads default title on the element", () => {
                let header = wrapper.find(".course-editor-hed > span")
                expect(header.text()).toEqual(defaultProps.title)
                expect(header.text()).toEqual(defaultProps.labels.new_course_title)
            })
        })

        describe("title is initially blank", () => {
            beforeEach(() => {
                loader({ title: ""})
            })

            it("loads empty", () => {
                expect(wrapper.hasProp('title', '')).toBe(true)
                expect(vm.title).toEqual('')
                expect(vm.course_title).toEqual(defaultProps.title)
            })

            it("loads default title on the element", () => {
                let header =  wrapper.find(".course-editor-hed > span")
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
                expect(wrapper.hasProp('title', title)).toBe(true)
                expect(vm.title).toEqual(title)
                expect(vm.course_title).toEqual(title)
            })

            it("loads the title on the element", () => {
                let header = wrapper.find(".course-editor-hed > span")
                expect(header.text()).toEqual(title)
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
                    expect(vm.$props.sections).toEqual( [{resources: []}] )
                    expect(vm.sections).toEqual( [{resources: []}] )
                    expect(vm.course_sections).toEqual( [{resources: []}] )
                    expect(vm.course_sections.length).toEqual(1)
                    expect(vm.course_sections instanceof Array).toBe(true)
                })

                xit("loads default section in the template", () => {
                    console.log(wrapper.html())
                    console.log(wrapper.contains(CourseSection))
                    console.log(vm.course_sections)
                    // expect(wrapper.contains(CourseSection)).toBe(true)
                })
            })
        })

        describe("sections are initially blank", () => {
            beforeEach(() => {
                loader({ sections: [] })
            })

            it("still loads default sections", () => {
                expect(vm.$props.sections).toEqual( [] )
                expect(vm.course_sections).toEqual( [{resources: []}] )
                expect(vm.course_sections.length).toEqual(1)
            })

            xit("loads default section in the template", () => {
                expect(wrapper.contains(CourseSection)).toBe(true)
            })
        })

        describe("sections are initially given", () => {
            let sections = [{resources: []}, {resources: []}]

            beforeEach(() =>{
                loader({ sections })
            })

            it("loads as a prop", () => {
                expect(vm.$props.sections).toEqual(sections)
                expect(vm.course_sections).toEqual(sections)
                expect(vm.course_sections.length).toEqual(2)
            })

            xit("loads sections into template", () => {
                expect(wrapper.contains(CourseSection)).toBe(true)
                expect(wrapper.findAll(CourseSection).length).toEqual(2)
            })
        })

        describe("Adding Sections", () => {
            beforeEach(() =>{
                loader()
            })

            it("adds a section", () => {
                expect(vm.course_sections.length).toEqual(1)
                vm.addSection()
                vm.addSection()
                expect(vm.course_sections.length).toEqual(3)
            })

            it("adds a section via the ui", () => {
                expect(vm.course_sections.length).toEqual(1)
                wrapper.find(".course-sections-add").trigger("click")
                expect(vm.course_sections.length).toEqual(2)
            })
        })

        describe("Subtracting Sections", () => {
            beforeEach(() =>{
                loader()
            })

            it("removes a section", () => {
                expect(vm.course_sections.length).toEqual(1)
                vm.removeSection(0)
                expect(vm.course_sections.length).toEqual(0)
            })

            it("removes a specific section", () => {
                expect(wrapper.vm.course_sections.length).toEqual(1)
                vm.addSection()
                vm.addSection()
                vm.addSection()
                vm.removeSection(3)
                expect(vm.course_sections.length).toEqual(3)
            })
        })

    })

    describe("Save a Course", () => {
        beforeEach(() => {
            let dProps = Object.assign({}, defaultProps)
            dProps = Object.assign(dProps, { id: 1, action: "update"})
            loader(dProps)
        })

        it("should save to db, and return an id", () => {
            expect(vm.course_id).toEqual(1)
            expect(vm.action).toEqual('update')
            expect(vm.savepoint).toEqual('/courses/1/')
            vm.saveCourse().then(
                () => {
                    expect(vm.course_id).toEqual(1)
                }
            )
        })

        it("should show a notification message on save", () => {
            expect(vm.course_id).toEqual(1)
            expect(vm.action).toEqual('update')
            expect(vm.savepoint).toEqual('/courses/1/')

            vm.saveCourse().then(
                () => {
                    expect(vm.alertStatus).toEqual('success')
                    expect(vm.alertMessage).toEqual('Your changes have been saved.')
                    expect(vm.alertUser).toBe(true)
                }
            )
        })
    })


    describe("Create a Course", () => {
        beforeEach(() => {
            let dProps = Object.assign({}, defaultProps)
            dProps.action = "create"
            loader(dProps)
        })

        it("should save to db, and return an id", () => {
            expect(vm.course_id).toBe(false)
            expect(vm.action).toEqual('create')
            vm.saveCourse().then(
                () => {
                    expect(vm.course_id).toEqual(1)
                }
            )
        })

        it("after saving, should change its save_action to 'update'", () => {
            expect(vm.save_action).toEqual('create')

            vm.saveCourse().then(
                () => {
                    expect(vm.save_action).toEqual('update')
                }
            )
        })

        it("after saving, should change its savepoint to the updatepoint", () => {
            expect(vm.savepoint).toEqual('.')

            vm.saveCourse().then(
                () => {
                    expect(vm.savepoint).toEqual('/courses/1/')
                }
            )
        })

        it("after saving, should change its save button label to reflect we are saving", () => {
            expect(wrapper.find(".course-save-ctrl-label").text()).toEqual(ORBLabels.create)

            vm.saveCourse().then(
                () => {
                    expect(wrapper.find(".course-save-ctrl-label").text()).toEqual(ORBLabels.save)
                }
            )
        })

        it("after saving, it should redirect the page to its new URL", () => {
            expect(vm.savepoint).toEqual('.')
            vm.saveCourse().then(
                () => {
                    expect(vm.savepoint).toEqual('/courses/1/')
                    expect(vm.redirectLogicCheck).toBe(true)
                }
            )
        })
    })
})
