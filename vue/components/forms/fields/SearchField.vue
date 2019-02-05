<script>
export default {
    name: "SearchField",
    props: {
        // @prop    value
        // @desc    string of search query
        value: {
            type: String,
            default: ""
        }
    },
    methods: {
        handleInput ({ target: { value } }) {
            this.$emit(
                "input",
                value
            )
        }
    }
}
</script>

<template>
<form
    class="form-group"
    @submit.prevent="$emit('submit')"
>
    <label for="search">
        <slot></slot>
    </label>

    <div class="input-group">
        <input
            class="form-control"
            id="search"
            :value="value"
            @input="handleInput"
        >

        <span class="input-group-btn">
            <button
                class="btn btn-info"
                type="submit"
            >
                {{ $i18n.SEARCH_LABEL }}
            </button>
        </span>
    </div>
</form>
</template>
