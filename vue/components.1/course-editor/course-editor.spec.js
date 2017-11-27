import { shallow } from 'vue-test-utils'
// import { shallow } from 'avoriaz'

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

describe('Course Editor', () => {
    let wrapper
    let vm
    let defaultProps = {
        title: 'New Course',
        status: 'draft',
        sections:  [{ resources: []}],
        labels: ORBLabels
    }

    function loader (
        propsD = defaultProps
    ){
        let propsData = Object.assign({}, propsD)
        wrapper = shallow(CourseEditor, { propsData })
        vm = wrapper.vm
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
            expect(wrapper.hasProp("sections", defaultProps.sections)).toBe(true)
            expect(wrapper.hasProp("labels", defaultProps.labels)).toBe(true)
        })
    })


    D       escribe("Course Title", () => {
        beforeEach(() => {
            loader()
        })

        it('can be passed as a property', () => {
            expect(CourseEditor.props.title).toBeDefined()
        })
    })
})


// it("can be edited", () => {
//     // error raises due to vue-test-utils
//     expect(vm.edit_head).toBe(false)
//     wrapper.find('.course-editor-hed-edit').trigger('click')
//     vm.editTitle()
//     wrapper.setData({ course_title: 'Test'})
//     expect(vm.edit_head).toBe(true)
// })
