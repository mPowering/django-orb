<script>
export default {
    name: "CourseActivity",
    props: {
        instance: {
            type: Object,
            default: () => ({})
        },
    },
    data () {
        return {
            activity: {
                ...this.instance
            },
            isEdittable: false,
        }
    },
    methods: {
        // @func    relayUpdate
        // @desc    inform parent of data change within section
        relayUpdate () {
            this.$emit("update", { resource: this.activity })
        },

        revertEditState ({ state = !this.isEdittable }) {
            this.activity = this.instance
            this.setEditState({ state })
        },

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

        <h5>{{ activity.title }}</h5>

        <slot name="entry:postheading"></slot>
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
                :id="`act_title_${ instance.uuid }`"
            >
        </div>

        <div class="form-group">
            <label :for="`act_desc_${ instance.uuid }`">
                {{ $i18n.ACTIVITY_DESC_LABEL }}
            </label>
            <textarea
                class="form-control"
                rows="10"
                v-model="activity.description"
                :id="`act_desc_${ instance.uuid }`"
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
