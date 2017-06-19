import Vue from 'vue'
import CourseEditor from './course-editor.vue'

let ORBLabels = {
    edit_title: "Edit Course Title",
    save_title: "Save Course Title"
}

describe('CourseEditor', () => {
    let vm
    let MockComponent = Vue.extend(CourseEditor)
    let defaultProps = {
        title: "New Course",
        sections: [],
        labels: ORBLabels
    }

    function loader (propsD = defaultProps) {
        let propsData = {}
        propsData = Object.assign(propsData, propsD)
        vm = new MockComponent({ propsData }).$mount()
    }
    
    describe("Initial Setup: ", () => {
        beforeEach(() => {
            loader()        
        })
        
        it('should be in the script', () => {
            expect(CourseEditor.name).toEqual('course-editor')
        })

        it('should mount', () => {
            expect(vm).toBeDefined()
        })  

        it('has a BeforeMount Hook', () => {
            expect(typeof CourseEditor.beforeMount).toBe('function')
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
                    expect(vm.$props.title).not.toBeDefined()
                    expect(vm.title).not.toBeDefined()
                    expect(vm.course_title).toEqual(defaultProps.title)
                })
                
                it("loads default title on the element", () => {
                    expect(
                        vm.$el.querySelector('.course-editor-hed').textContent
                    )
                    .toEqual(defaultProps.title)
                })
            })

            describe("title is initially blank", () => {
                beforeEach(() => {
                    loader({ title: ""})
                })

                it("loads empty", () => {
                    expect(vm.$props.title).toEqual('')
                    expect(vm.title).toEqual('')
                    expect(vm.course_title).toEqual(defaultProps.title)
                })
                
                it("loads default title on the element", () => {
                    expect(
                        vm.$el.querySelector('.course-editor-hed').textContent
                    )
                    .toEqual(defaultProps.title)
                })
            })

            describe("title is initially given", () => {
                let title = "Test Title"
                beforeEach(() => {
                    loader({ title })
                })
                
                it("loads as prop", () => {
                    expect(vm.$props.title).toEqual(title)
                    expect(vm.title).toEqual(title)
                    expect(vm.course_title).toEqual(title)
                })

                it("loads the title on the element", () => {
                    expect(
                        vm.$el.querySelector('.course-editor-hed').textContent
                    )
                    .toEqual(title)
                })
            })

            it("can be edited", () => {
                expect(vm.edit_head).toBe(false)
                vm.editTitle()
                vm.course_title = "Test"
                expect(vm.edit_head).toBe(true)
                expect(vm.course_title).toEqual("Test")
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
                    expect(vm.$props.sections).not.toBeDefined()
                    expect(vm.sections).not.toBeDefined()
                    expect(vm.course_sections).toEqual(defaultProps.sections)
                    expect(vm.course_sections.length).toEqual(0)
                    expect(vm.$data.course_sections instanceof Array).toBe(true)
                    
                })
                
                xit("loads default section in the template", () => {
                })
            })

            describe("sections are initially blank", () => {
                beforeEach(() => {
                    loader({ sections: []})
                })

                it("loads empty", () => {
                    expect(vm.$props.sections).toBeDefined()
                    expect(vm.sections).toEqual([])
                    expect(vm.course_sections).toEqual(defaultProps.sections)
                    expect(vm.course_sections.length).toEqual(0)
                })
                
                xit("loads default section in the template", () => {
                    expect(
                        vm.$el.querySelector('.course-editor-hed').textContent
                    )
                    .toEqual(defaultProps.title)
                })
            })

            describe("sections are initially given", () => {
                let sections = [[], []]
                beforeEach(() => {
                    loader({ sections })
                })
                
                it("loads as prop", () => {
                    expect(vm.$props.sections).toEqual(sections)
                    expect(vm.sections).toEqual(sections)
                    expect(vm.course_sections).toEqual(sections)
                    expect(vm.course_sections.length).toEqual(2)
                })

                xit("loads the sections in the template", () => {
                    expect(
                        vm.$el.querySelector('.course-editor-hed').textContent
                    )
                    .toEqual(title)
                })
            })
        })
    })

    xdescribe("Course Form Labels", () => {
        it('is a property', () => {
            expect(CourseEditor.props.labels).toBeDefined()
        })


    })
})
