<script>
export default {
    name: "CourseActivity",
    props: {
        canEdit: {
            type: Boolean,
            default: false
        },
        // @prop    instance
        // @desc    individual activity instance assigned to a course section
        instance: {
            type: Object,
            default: () => ({})
        },
    },
    data () {
        return {
            // @prop    activity
            // @desc    initiate local activity from passed prop
            activity: {
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
            this.$emit("update", { resource: this.activity })
        },

        // @func    revertEditState
        // @desc    if user cancels edit,
        // @        revert the local data to the passed instance
        // @        and turn editing off
        revertEditState ({ state = !this.isEdittable }) {
            this.activity = this.instance

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
<div class="course-activity panel panel-info iso:yEnd0 edge:xyEq">
    <header
        class="course-activity-hdr panel-heading flex:h--p:start--s:middle pad:xyEq25 rhy:xStart25"
        v-if="!isEdittable"
    >
        <slot name="preheading"></slot>

        <h5 class="iso:yEq0">{{ activity.title }}</h5>

        <slot name="postheading"></slot>
    </header>

    <div
        class="panel-body"
        v-if="isEdittable"
    >
        <div class="form-group">
            <label :for="`act_title_${ activity.uuid }`">
                {{ $i18n.ACTIVITY_TITLE_LABEL }}
            </label>

            <input
                class="form-control"
                type="text"
                v-model="activity.title"
                :id="`act_title_${ activity.uuid }`"
            >
        </div>

        <div class="form-group">
            <label :for="`act_desc_${ activity.uuid }`">
                {{ $i18n.ACTIVITY_DESC_LABEL }}
            </label>
            <textarea
                class="form-control"
                rows="10"
                v-model="activity.description"
                :id="`act_desc_${ activity.uuid }`"
            ></textarea>
        </div>
    </div>

    <template v-else>
        <div
            class="panel-body"
            v-if="activity.description"
        >
            {{ activity.description }}
        </div>
    </template>

    <footer class="panel-footer flex:h--p:end--s:middle rhy:xStart50" v-if="canEdit">
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
