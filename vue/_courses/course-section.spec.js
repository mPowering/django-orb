// import Vue from 'vue'
// import CourseSection from './course-section.vue'

// let ORBLabels = {
//     edit_title: "Edit Course Title",
//     save_title: "Save Course Title"
// }

// describe('CourseEditor', () => {
//     let vm
//     let MockComponent = Vue.extend(CourseSection)
//     let defaultProps = {
//         resources: [],
//         labels: ORBLabels
//     }

//     function loader (propsD = defaultProps) {
//         let propsData = {}
//         propsData = Object.assign(propsData, propsD)
//         vm = new MockComponent({ propsData }).$mount()
//     }
    
//     describe("Initial Setup: ", () => {
//         beforeEach(() => {
//             loader()        
//         })
        
//         it('should be in the script', () => {
//             expect(CourseSection.name).toEqual('course-section')
//         })

//         it('should mount', () => {
//             expect(vm).toBeDefined()
//         })  

//         // it('has a BeforeMount Hook', () => {
//         //     expect(typeof CourseEditor.beforeMount).toBe('function')
//         // })
//     })

    
// })
