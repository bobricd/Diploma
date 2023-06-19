from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Swipe.residential_complexes.views import ResidentialComplexCreateView, ResidentialComplexDetailView, \
    ResidentialComplexListView, DocumentCreateView, AddFavouriteResidentialComplexView, \
    RemoveFavouriteResidentialComplexView, NewsCreateView, SectionViewSet, BlockViewSet, RiserViewSet, FloorViewSet,\
    AdvantageViewSet

router = DefaultRouter()
router.register(r'blocks', BlockViewSet, basename="residential_complex_block")
router.register(r'sections', SectionViewSet, basename="residential_complex_section")
router.register(r'floors', FloorViewSet, basename="residential_complex_floor")
router.register(r'risers', RiserViewSet, basename="residential_complex_riser")
router.register(r'advantages', AdvantageViewSet, basename="residential_complex_advantage")

urlpatterns = [
    path('', include(router.urls)),
    path('document/create/', DocumentCreateView.as_view(), name="document_create"),
    path('news/create/', NewsCreateView.as_view(), name="news_create"),
    path('list/', ResidentialComplexListView.as_view(), name="residential_complex_list"),
    path('create/', ResidentialComplexCreateView.as_view(), name="residential_complex_create"),
    path('profile/', ResidentialComplexDetailView.as_view(), name="residential_complex_detail"),
    path('add-to-favourite/<int:pk>/', AddFavouriteResidentialComplexView.as_view(),
         name="residential_complex_add_fav"),
    path('remove-from-favourite/<int:pk>/', RemoveFavouriteResidentialComplexView.as_view(),
         name="residential_complex_remove_fav"),

]
