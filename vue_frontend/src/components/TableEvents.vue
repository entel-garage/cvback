<template>
  <div class="fit">
    <div class="fit column no-wrap justify-between items-start content-start">
      <div
        class="fit row reverse wrap justify-between items-end content-between barlow-bold"
        style="
          margin: 0;
          padding: 0;
          border-top: 1px solid rgba(0, 0, 0, 0.12);
          border-left: 1px solid rgba(0, 0, 0, 0.12);
          border-right: 1px solid rgba(0, 0, 0, 0.12);
        "
      >
        <q-btn
          v-if="homeView"
          id="btn-sort-sm"
          class="lt-md"
          dense
          flat
          no-caps
          color="primary"
          label="Ordenar"
          style="width: 150px"
          :icon-right="eventStore.sortAsc ? 'arrow_downward' : 'arrow_upward'"
          @click="eventSort(false)"
        />

        <!-- <q-btn no-caps color="primary" label="Exportar data" class="q-px-xl" :loading="loadingExport" @click="exportData()" /> -->
        <q-btn-dropdown
          no-caps
          color="primary"
          label="Exportar data"
          class="q-px-xl"
          style="width: 150px"
          :loading="loadingExport"
        >
          <q-list separator class="fit">
            <q-item clickable v-close-popup class="text-right fit" @click="exportData('csv')">
              <q-item-section>
                <q-item-label> Formato .csv</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-close-popup class="text-right fit" @click="exportData('xlsx')">
              <q-item-section>
                <q-item-label> Formato .xlsx</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
      <div class="gt-sm fit col-12">
        <q-table
          class="fit my-sticky-dynamic fs-15-18"
          flat
          bordered
          :rows="displayRows"
          :columns="columns"
          row-key="id"
          :loading="loading"
          v-model:expanded="expanded"
          :pagination.sync="eventStore.pagination"
          header-class="text-dark"
          hide-pagination
        >
          <template v-slot:header-cell-date="props">
            <q-th :props="props" style="padding-left: 0px">
              <q-btn
                v-if="homeView"
                flat
                round
                color="primary"
                :icon="eventStore.sortAsc ? 'arrow_downward' : 'arrow_upward'"
                @click="eventSort(false)"
              />
              {{ props.col.label }}
            </q-th>
          </template>

          <template v-slot:body="props">
            <q-tr
              :props="props"
              :class="colorRowSelected(props.row)"
              class="text-grey-14"
              @click="getRowSelected(props.row)"
            >
              <q-td key="name" :props="props">
                <span class="barlow-semibold fs-15-18 q-pl-lg">
                  {{ props.row.eventType.name }}
                </span>
              </q-td>
              <q-td key="date" :props="props">
                <span class="barlow-semibold fs-15-18">
                  {{ formatDateEvent(props.row.addedDate).date }}
                </span>

                <span class="fs-15-18"> | {{ formatDateEvent(props.row.addedDate).time }}</span>
              </q-td>
              <q-td key="name" :props="props" class="text-center">
                <span class="barlow-semibold fs-15-18">
                  {{ props.row.eventLabel.name }}
                </span>
              </q-td>
              <q-td class="text-rigth">
                <q-btn
                  size="sm"
                  color="accent"
                  round
                  dense
                  :icon="props.expand ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                />
              </q-td>
            </q-tr>
            <q-tr v-show="props.expand" :props="props">
              <q-td colspan="100%" class="no-padding">
                <div
                  class="fit row justify-between q-py-sm"
                  style="min-height: 500px; overflow-y: auto"
                >
                  <div class="col-4 text-left q-pa-md q-gutter-md">
                    <q-list class="fit">
                      <q-item v-if="props.row.confidence">
                        <q-item-section>
                          <q-item-label
                            >Confiabilidad:
                            <span class="barlow-bold">
                              {{ toPercentage(props.row.confidence) }}%
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Fecha creado:
                            <span class="barlow-bold">
                              {{ formatDateEvent(props.row.addedDate).date }}
                            </span>
                            <span class="barlow">
                              | {{ formatDateEvent(props.row.addedDate).time }}
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Fecha informado:
                            <span class="barlow-bold">
                              {{ formatDateEvent(props.row.informedDate).date }}
                            </span>
                            <span class="barlow">
                              | {{ formatDateEvent(props.row.informedDate).time }}
                            </span>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >OCR:
                            <div v-if="props.row.inferenceOcr.length >= 1">
                              <div v-for="ocr in props.row.inferenceOcr" :key="ocr.id">
                                <q-chip dense outline color="blue-5" class="barlow q-py-sm q-px-sm"
                                  >{{ ocr.name }}: <span class="barlow-bold">{{ ocr.value }} </span>
                                </q-chip>
                              </div>
                            </div>
                            <div v-else style="max-width: fit-content">
                              <q-chip dense outline color="blue-5" class="barlow q-px-sm q-pt-xs">
                                No identificado
                              </q-chip>
                            </div>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label
                            >Clasificación:
                            <div v-if="props.row.inferenceClassification.length >= 1">
                              <div
                                v-for="inference in props.row.inferenceClassification"
                                :key="inference.id"
                              >
                                <q-chip dense outline color="blue-5" class="barlow q-py-sm q-px-sm"
                                  >{{ addTextToClassification(inference.label.name) }}
                                </q-chip>
                              </div>
                            </div>
                            <div v-else style="max-width: fit-content">
                              <q-chip dense outline color="blue-5" class="barlow q-px-sm q-pt-xs">
                                No identificado
                              </q-chip>
                            </div>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section>
                          <q-item-label>Etiquetas: </q-item-label>

                          <q-chip
                            outline
                            v-for="label in props.row.labelsDetected"
                            :key="label.id"
                            :label="label.name"
                            icon="check_circle"
                            color="positive"
                            style="max-width: fit-content"
                            class="q-px-xs"
                          />
                          <q-chip
                            outline
                            v-for="label in props.row.labelsMissing"
                            :key="label.id"
                            :label="label.name"
                            icon="cancel"
                            color="negative"
                            style="max-width: fit-content"
                            class="q-px-xs"
                          />
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <div class="col-8">
                    <CarouselImages
                      :frames="props.row.frames"
                      :inferenceDetectionClassification="props.row.inferenceDetectionClassification"
                      :videos="props.row.videos"
                      :eventSelected="expanded"
                    />
                  </div>
                </div>
              </q-td>
            </q-tr>
          </template>
        </q-table>
        <div class="q-pa-lg flex flex-center">
          <q-pagination
          v-if="homeView"
            :model-value="eventStore.pagination.page"
            direction-links
            ellipses
            :max="pagesNumber"
            :max-pages="7"
            text-color="dark"
            active-text-color="white"
            color="dark"
            class="q-px-xl"
            style="max-width: fit-content"
            @update:model-value="updatePagination"
          />
        </div>
      </div>
    </div>

    <div class="lt-md">
      <q-list v-if="displayRows.length === 0" bordered>
        <q-item> No hay datos para mostrar </q-item>
      </q-list>
      <q-list v-else bordered separator class="rounded-borders">
        <q-expansion-item :default-opened="!homeView" group="events" bordered v-for="row in displayRows" :key="row.id">
          <template v-slot:header>
            <q-item-section class="column">
              <q-item-label class="barlow-bold text-dark fs-21-25 q-py-sm">
                {{ row.eventType.name }}
              </q-item-label>

              <q-item-label class="fs-14-19 text-dark">
                <span class="barlow-semibold fs-15-18">
                  {{ formatDateEvent(row.addedDate).date }}
                </span>

                <span class="fs-15-18"> | {{ formatDateEvent(row.addedDate).time }}</span>
              </q-item-label>
              <q-item-label class="barlow text-dark fs-21-25 q-py-sm">
                {{ row.eventLabel.name }}
              </q-item-label>
            </q-item-section>
          </template>

          <q-card>
            <q-card-section>
              <q-item-label v-if="row.confidence" class="text-dark fs-14-19 q-py-sm"
                >Confiabilidad:
                <span class="barlow-bold fs-15-18"> {{ toPercentage(row.confidence) }}% </span>
              </q-item-label>
              <q-item-label
                >Fecha creado:
                <span class="barlow-bold">
                  {{ formatDateEvent(row.addedDate).date }}
                </span>
                <span class="barlow"> | {{ formatDateEvent(row.addedDate).time }} </span>
              </q-item-label>
              <q-item-label
                >Fecha informado:
                <span class="barlow-bold">
                  {{ formatDateEvent(row.informedDate).date }}
                </span>
                <span class="barlow"> | {{ formatDateEvent(row.informedDate).time }} </span>
              </q-item-label>
              <q-item-label v-if="row.inferenceOcr.length >= 1"
                >OCR:
                <div v-for="ocr in row.inferenceOcr" :key="ocr.id">
                  <q-chip dense outline color="blue-5" class="barlow q-py-sm q-px-sm"
                    >{{ ocr.name }}: <span class="barlow-bold">{{ ocr.value }} </span>
                  </q-chip>
                </div>
              </q-item-label>
              <q-item-label v-else>
                OCR:
                <q-chip dense outline color="blue-5" class="barlow q-px-sm q-pt-xs"
                  >No identificado
                </q-chip>
              </q-item-label>
              <q-item-label v-if="row.inferenceClassification.length >= 1"
                >Clasificación:
                <div v-for="inference in row.inferenceClassification" :key="inference.id">
                  <q-chip dense outline color="blue-5" class="barlow q-py-sm q-px-sm">
                    {{ addTextToClassification(inference.label.name) }}
                  </q-chip>
                </div>
              </q-item-label>
              <q-item-label v-else>
                Clasificación:
                <q-chip dense outlinecolor="blue-5" class="barlow q-px-sm q-pt-xs">
                  No identificado
                </q-chip>
              </q-item-label>
              <q-item-label
                >Etiquetas:
                <div>
                  <q-chip
                    outline
                    v-for="label in row.labelsDetected"
                    :key="label.id"
                    :label="label.name"
                    icon="check_circle"
                    color="positive"
                    style="max-width: fit-content"
                    class="q-px-xs"
                  />
                  <q-chip
                    outline
                    v-for="label in row.labelsMissing"
                    :key="label.id"
                    :label="label.name"
                    icon="cancel"
                    color="negative"
                    style="max-width: fit-content"
                    class="q-px-xs"
                  />
                </div>
              </q-item-label>
            </q-card-section>
            <q-card-section>
              <CarouselImages
                :frames="row.frames"
                :inferenceDetectionClassification="row.inferenceDetectionClassification"
                :videos="row.videos"
                :frameSelected="rowSelected"
              />
            </q-card-section>
          </q-card>
        </q-expansion-item>

        <q-separator />
      </q-list>
      <div class="q-pa-lg flex flex-center">
        <q-pagination
        v-if="homeView"
          :model-value="eventStore.pagination.page"
          direction-links
          ellipses
          :max="pagesNumber"
          :max-pages="5"
          text-color="dark"
          active-text-color="white"
          color="dark"
          class="q-px-xl"
          @update:model-value="updatePagination"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch, onMounted } from 'vue'
import { types } from '@/utils/colors'
import { useEventsStore } from '@/stores/events'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'


import CarouselImages from '@/components/CarouselImages.vue'

export default defineComponent({
  name: 'TableEvents',
  emits: ['sortAsc'],
  props: ['rows', 'columns', 'loading', 'homeView'],
  components: {
    CarouselImages
  },
  setup(props, { emit }) {
    const routes = useRouter()
    const eventIdFromURL = routes.currentRoute.value.params.eventid
  
    const rowSelected = ref(null)
    const slide = ref(1)
    const fullscreen = ref(false)
    const expanded = ref([])

    const eventStore = useEventsStore()
    const $q = useQuasar()
    const sortAsc = ref(true)

    if(eventIdFromURL){
      expanded.value = [eventIdFromURL]
      rowSelected.value = props.rows.find(row => row.id === eventIdFromURL)
    }


    const eventSort = () => {
      sortAsc.value = !sortAsc.value
      emit('sortAsc', sortAsc.value)
    }

  
    const pagesNumber = computed(() => {
      const totalToUse = eventStore.summaryEvents?.totalQueryEvents
      return totalToUse ? Math.ceil(totalToUse / eventStore.pagination.rowsPerPage) : 1
    })

    const displayRows = computed(() => {
      return props.rows ? props.rows : []
    })

    const getRowSelected = (row, column, event) => {
      console.log("row", row)
      if (rowSelected.value?.id === row.id) {
        rowSelected.value = null
        expanded.value = []
      } else {
        rowSelected.value = row
        expanded.value = [row.id]
      }
    }

    const formatDateEvent = (date) => {
      const dateObj = new Date(date)

      const month =
        dateObj.getMonth() + 1 < 10 ? `0${dateObj.getMonth() + 1}` : dateObj.getMonth() + 1
      const day = dateObj.getDate() < 10 ? `0${dateObj.getDate()}` : dateObj.getDate()
      const year = dateObj.getFullYear()
      const hour = dateObj.getHours() < 10 ? `0${dateObj.getHours()}` : dateObj.getHours()
      const minutes = dateObj.getMinutes() < 10 ? `0${dateObj.getMinutes()}` : dateObj.getMinutes()
      const seconds = dateObj.getSeconds() < 10 ? `0${dateObj.getSeconds()}` : dateObj.getSeconds()

      const newDate = {
        date: `${day}/${month}/${year}`,
        time: `${hour}:${minutes}:${seconds}`
      }
      return newDate
    }

    const colorRowSelected = (row) => {
      if (rowSelected.value?.id === row.id) {
        return 'bg-blue-3'
      }
    }

    const toggleExpand = (row, event) => {
      event.stopPropagation()
      getRowSelected(row, event)
    }

    const toPercentage = (value) => {
      return value * 100
    }

    const findColor = (value) => {
      const color = types[value.colorGroup.toLowerCase()]

      if (color == '#000000') {
        return `background-color: ${color}; border: 2px solid ${color}; color: white`
      } else {
        return `background-color: ${color}; border: 2px solid ${color};`
      }
    }

    const updatePagination = async (value) => {
      eventStore.pagination.page = value
      eventStore.pagination.offset =
        eventStore.pagination.page * eventStore.pagination.rowsPerPage -
        eventStore.pagination.rowsPerPage
    }

    const exportData = async (format) => {
      const response = eventStore.EXPORT_DATA(format)

      if (response) {
        $q.notify({
          message:
            'Tu solicitud esta siendo procesada. Te enviaremos un correo en los próximos minutos con la confirmación',
          color: 'positive',
          position: 'bottom',
          timeout: 2000
        })
      }
    }
    const loadingExport = computed(() => {
      return eventStore.loadingExport
    });

    const addTextToClassification = (value) => {
      if (value === 'orange') {
        return 'Banderín en buen estado'
      } else if (value === 'not_orange') {
        return 'Banderín en mal estado'
      } else {
        return value
      }
    }

    return {
      rowSelected,
      pagesNumber,
      getRowSelected,
      formatDateEvent,
      colorRowSelected,
      slide,
      fullscreen,
      expanded,
      toggleExpand,
      toPercentage,
      findColor,
      eventStore,
      updatePagination,
      displayRows,
      exportData,
      loadingExport,
      eventSort,
      addTextToClassification
    }
  }
})
</script>

<style lang="scss">
.q-pagination__middle.row.justify-center {
  max-width: fit-content !important;
}
.my-sticky-dynamic {
  /* height or max-height is important */
  height: 60vh;

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th /* bg color is important for th; just specify one */ {
    background-color: #ffffff;
  }

  thead tr th {
    position: sticky;
    z-index: 2;
    color: #4a4a4a;
  }

  /* this will be the loading indicator */
  thead tr:last-child th {
    /* height of all previous header rows */
    top: 48px;
    font-size: 16px;
    line-height: 19px;
    font-weight: 600;
    color: #4a4a4a;
  }

  thead tr:first-child th {
    top: 0;
    padding-left: 30px;
  }

  /* prevent scrolling behind sticky top row on focus */
  tbody {
    /* height of all previous header rows */
    scroll-margin-top: 48px;
    color: #828282;
  }

  .q-table--horizontal-separator tbody tr > td {
    padding-left: 50px;
  }

  tbody tr:nth-child(odd) {
    // Add this selector
    background-color: #fafafa; // Add your desired color here
  }
}
.q-focus-helper {
  display: none !important;
}
.q-field__control-container {
  min-width: 200px !important;
}
#btn-sort-sm .q-btn__content {
  padding-left: 20px;
}
#btn-sort-sm span.block {
  width: fit-content;
}
</style>
