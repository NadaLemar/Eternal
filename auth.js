document.addEventListener('DOMContentLoaded', () => {
  EterItemGrid.mount({
    dataPath: 'data/armors.json',
    gridId: 'ar-grid',
    tabsId: 'ar-tabs',
    tabField: 'type',
    searchId: 'ar-search',
    countId: 'ar-count',
    showImage: true,
    catKey: 'armors',
    filters: [
      { id: 'ar-cat1', field: 'category1' },
      { id: 'ar-grade', field: 'grade', isGrade: true },
    ],
  });
});
