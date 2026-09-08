document.addEventListener('DOMContentLoaded', () => {
  EterItemGrid.mount({
    dataPath: 'data/costume_items.json',
    gridId: 'ci-grid',
    tabsId: 'ci-tabs',
    tabField: 'type',
    searchId: 'ci-search',
    countId: 'ci-count',
    showImage: true,
    filters: [
      { id: 'ci-grade', field: 'grade', isGrade: true },
    ],
  });
});
