// @func    parseTemplateData
// @desc    used to parse json data embedded within a server delivered template
export const parseTemplateData = ({ id, required = false }) => {
    try {
        let element = document.getElementById(id)

        // @info    we don't have this in the template
        // @        if required, lets throw an error
        // @        else fail silently as we might just have it as an optional load
        if (!element && required) throw `[ORB Error] Template data of #${ id } is not in template and is marked as required.`
        if (!element) return

        return JSON.parse(element.innerHTML)
    }
    catch (err) {
        console.error(err)
        return false
    }
}
