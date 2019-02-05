<script>
export default {
    name: "CourseActivity",
    props: {
        // @prop    instance
        // @desc    individual activity instance assigned to a course section
        instance: {
            type: Object,
            default: () => ({})
        },
    },
    data () {
        return {
            // @prop    currentActivity
            // @desc    initiate local activity from passed prop
            currentActivity: {
                ...this.instance
            },

            // @prop    isEdittable
            // @desc    state for
            isEdittable: false,
        }
    },
    methods: {
        // @func    relayUpdate
        // @desc    inform parent of data change within section
        relayUpdate () {
            this.$emit("update", { resource: this.currentActivity })
        },

        // @func    revertEditState
        // @desc    if user cancels edit,
        // @        revert the local data to the passed instance
        // @        and turn editing off
        revertEditState ({ state = !this.isEdittable }) {
            this.currentActivity = this.instance

            this.setEditState({ state })
        },

        // @func    setEditState
        // @desc    toggle the edit state
        // @        if we toggle to "off", inform the parent of our updates
        setEditState ({ state = !this.isEdittable }) {
            this.isEdittable = state

            if (!state) this.relayUpdate()
        },


    }
}
</script>

<template>
<div class="course-activity panel panel-info edge:xyEq">
    <header
        class="course-activity-hdr panel-heading flex:h--p:start--s:middle rhy:xStart25"
        v-if="!isEdittable"
    >
        <slot name="entry:preheading"></slot>

        <h5>{{ currentActivity.title }}</h5>

        <slot name="entry:postheading"></slot>
    </header>

    <div
        class="panel-body"
        v-if="isEdittable"
    >
        <div class="form-group">
            <label :for="`act_title_${ currentActivity.uuid }`">
                {{ $i18n.ACTIVITY_TITLE_LABEL }}
            </label>

            <input
                class="form-control"
                type="text"
                v-model="currentActivity.title"
                :id="`act_title_${ currentActivity.uuid }`"
            >
        </div>

        <div class="form-group">
            <label :for="`act_desc_${ currentActivity.uuid }`">
                {{ $i18n.ACTIVITY_DESC_LABEL }}
            </label>
            <textarea
                class="form-control"
                rows="10"
                v-model="currentActivity.description"
                :id="`act_desc_${ currentActivity.uuid }`"
            ></textarea>
        </div>
    </div>

    <template v-else>
        <div
            class="panel-body"
            v-if="currentActivity.description"
        >
            {{ currentActivity.description }}
        </div>
    </template>

    <footer class="panel-footer flex:h--p:end--s:middle rhy:xStart50">
        <template v-if="isEdittable">
            <action-control
                glyph="ban-circle"
                theme="danger"
                @click="revertEditState"
            >
                <span>{{ $i18n.ACTIVITY_CANCEL }}</span>
            </action-control>
            <action-control
                glyph="ok-circle"
                theme="success"
                @click="setEditState"
            >
                <span>{{ $i18n.ACTIVITY_SAVE }}</span>
            </action-control>
        </template>

        <template v-else>
            <action-control
                glyph="edit"
                theme="primary"
                @click="setEditState"
            >
                <span>{{ $i18n.ACTIVITY_EDIT }}</span>
            </action-control>
        </template>
    </footer>
</div>
</template>
