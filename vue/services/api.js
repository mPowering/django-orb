// @thirdparty Axios declaration
// set up CSRF for use with Django.Python server
// vue-resource is "depreciated;
// seeL https://medium.com/the-vue-point/retiring-vue-resource-871a82880af4
import Axios from "axios"
Axios.defaults.xsrfCookieName = "csrftoken"
Axios.defaults.xsrfHeaderName = "X-CSRFToken"

class API {
    constructor () {
        this.name = "API"
    }

    // @func    delete
    // @desc    send DELETE method to server
    // @info    server system will supply responses,
    // @        try/catch only revolves around browser-side issues
    async delete ({ route }) {
        try {
            if (!route) return "Route must be sent as an object!"
            let { data } = await AXIOS.delete(route)
            return data
        }
        catch (err) {
            // @info   if there is an error before we get to the server,
            // @        supply a response to ui
            return {
                error: true,
                message: "Deletion not currently available. Please try again later."
            }
        }
    }

    async fetch ({ route, params = "" }) {
        if (!route) return "Route must be sent as an object!"
        try {
            let { data } = await Axios.get(route, { params })
            return data
        }
        catch (error) { return }
    }

    async update ({ route, data }) {
        if (!route) return "Route must be sent as an object!"
        try {
            let { data: response } = await Axios.post(route, data)
            return response
        }
        catch (error) { return }
    }
}

export const api = new API()
