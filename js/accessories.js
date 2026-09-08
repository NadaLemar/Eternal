document.addEventListener('DOMContentLoaded', () => {
  EterItemGrid.mount({
    dataPath: 'data/accessories.json',
    gridId: 'ac-grid',
    tabsId: 'ac-tabs',
    tabField: 'type',
    searchId: 'ac-search',
    countId: 'ac-count',
    showImage: true,
    filters: [
      { id: 'ac-cat1', field: 'category1' },
      { id: 'ac-grade', field: 'grade', isGrade: true },
    ],
  });
});
