from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

class ChartResponseSerializer(InheritedSerializer):
    CHITIEU = serializers.CharField(help_text="`CHITIEU` of data")
    SODU_DS_LK_KYT = serializers.CharField(help_text="`SODU_DS_LK_KYT` of data")
    THUC_HIEN_KY_T = serializers.CharField(help_text="`THUC_HIEN_KY_T` of data")
    KE_HOACH_KY_T = serializers.CharField(help_text="`KE_HOACH_KY_T` of data")
    TYLE_KY_T = serializers.CharField(help_text="`TYLE_KY_T` of data")
    THUC_HIEN_LK = serializers.CharField(help_text="`THUC_HIEN_LK` of data")
    KE_HOACH_LK = serializers.CharField(help_text="`KE_HOACH_LK` of data")
    TY_LY_LK = serializers.CharField(help_text="`TY_LY_LK` of data")
    DIEM_CHI_TIEU_LK = serializers.CharField(help_text="`DIEM_CHI_TIEU_LK` of data")
    DIEM_KH_LK = serializers.CharField(help_text="`DIEM_KH_LK` of data")
    KH_NAM = serializers.CharField(help_text="`KH_NAM` of data")
    TY_LE_NAM = serializers.CharField(help_text="`TY_LE_NAM` of data")
    DIEM_CHI_TIEU_KH_NAM = serializers.CharField(help_text="`DIEM_CHI_TIEU_KH_NAM` of data")
    DIEM_KH_NAM = serializers.CharField(help_text="`DIEM_KH_NAM` of data")
    AMOUNT_CHART = serializers.CharField(help_text="`AMOUNT_CHART` of data")

class PFSChartResponseSerializer(InheritedSerializer):
    Tang_truong_huy_dong_binh_quan_ckh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Tang_truong_huy_dong_binh_quan_ckh_ty_le_htkh_luy_ke` of data")
    Tang_truong_huy_dong_binh_quan_ckh_diem = serializers.CharField(help_text="`Tang_truong_huy_dong_binh_quan_ckh_diem` of data")
    Tang_truong_huy_dong_binh_quan_kkh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Tang_truong_huy_dong_binh_quan_kkh_ty_le_htkh_luy_ke` of data")
    Tang_truong_huy_dong_binh_quan_kkh_diem = serializers.FloatField(help_text="`Tang_truong_huy_dong_binh_quan_kkh_diem` of data")
    Doanh_so_giai_ngan_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Doanh_so_giai_ngan_ty_le_htkh_luy_ke` of data")
    Doanh_so_giai_ngan_diem = serializers.FloatField(help_text="`Doanh_so_giai_ngan_diem` of data")
    Thu_phi_dich_vu_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Thu_phi_dich_vu_ty_le_htkh_luy_ke` of data")
    Thu_phu_dich_vu_diem = serializers.FloatField(help_text="`Thu_phu_dich_vu_diem` of data")
    Loi_nhuan_truoc_thue_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Loi_nhuan_truoc_thue_ty_le_htkh_luy_ke` of data")
    Loi_nhuan_truoc_thue_diem = serializers.FloatField(help_text="`Loi_nhuan_truoc_thue_diem` of data")
    Doanh_so_bao_hiem_nhan_tho_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Doanh_so_bao_hiem_nhan_tho_ty_le_htkh_luy_ke` of data")
    Doanh_so_bao_hiem_nhan_tho_diem = serializers.FloatField(help_text="`Doanh_so_bao_hiem_nhan_tho_diem` of data")
    So_luong_the_tdqt_phat_hanh_moi_ty_le_htkh_luy_ke = serializers.CharField(help_text="`So_luong_the_tdqt_phat_hanh_moi_ty_le_htkh_luy_ke` of data")
    So_luong_the_tdqt_phat_hanh_moi_diem = serializers.FloatField(help_text="`So_luong_the_tdqt_phat_hanh_moi_diem` of data")
    So_du_trai_phieu_binh_quan_ty_le_htkh_luy_ke = serializers.CharField(help_text="`So_du_trai_phieu_binh_quan_ty_le_htkh_luy_ke` of data")
    So_du_trai_phieu_binh_quan_diem = serializers.FloatField(help_text="`So_du_trai_phieu_binh_quan_diem` of data")
    Phat_trien_khach_hang_moi_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Phat_trien_khach_hang_moi_ty_le_htkh_luy_ke` of data")
    Phat_trien_khach_hang_moi_diem = serializers.FloatField(help_text="`Phat_trien_khach_hang_moi_diem` of data")

class EnterpriseChartResponseSerializer(InheritedSerializer):
    Tang_truong_huy_dong_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Tang_truong_huy_dong_ty_le_htkh_luy_ke` of data")
    Tang_truong_huy_dong_ty_le_htkh_diem = serializers.FloatField(help_text="`Tang_truong_huy_dong_ty_le_htkh_diem` of data")
    Tang_truong_huy_dong_von_binh_quan_kkh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Tang_truong_huy_dong_von_binh_quan_kkh_ty_le_htkh_luy_ke` of data")
    Tang_truong_huy_dong_von_binh_quan_kkh_diem = serializers.FloatField(help_text="`Tang_truong_huy_dong_von_binh_quan_kkh_diem` of data")
    Tang_truong_cho_vay_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Tang_truong_cho_vay_ty_le_htkh_luy_ke` of data")
    Tang_truong_cho_vay_diem = serializers.FloatField(help_text="`Tang_truong_cho_vay_diem` of data")
    Tang_truong_cho_vay_binh_quan_ty_le_ktkh_luy_ke = serializers.CharField(help_text="`Tang_truong_cho_vay_binh_quan_ty_le_ktkh_luy_ke` of data")
    Tang_truong_cho_vay_binh_quan_diem = serializers.FloatField(help_text="`Tang_truong_cho_vay_binh_quan_diem` of data")
    Thu_phi_dich_vu_ty_le_ktkh_luy_ke = serializers.CharField(help_text="`Thu_phi_dich_vu_ty_le_ktkh_luy_ke` of data")
    Thu_phi_dich_vu_diem = serializers.FloatField(help_text="`Thu_phi_dich_vu_diem` of data")
    Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke` of data")
    Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_diem = serializers.FloatField(help_text="`Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_diem` of data")
    Thu_phi_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Thu_phi_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke` of data")
    Thu_phi_ttqt_va_ln_kdnh_diem = serializers.FloatField(help_text="`Thu_phi_ttqt_va_ln_kdnh_diem` of data")
    Doanh_so_thanh_toan_qr_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Doanh_so_thanh_toan_qr_ty_le_htkh_luy_ke` of data")
    Doanh_so_thanh_toan_qr_diem = serializers.FloatField(help_text="`Doanh_so_thanh_toan_qr_diem` of data")
    So_luong_merchant_qr_ty_le_htkh_luy_ke = serializers.CharField(help_text="`So_luong_merchant_qr_ty_le_htkh_luy_ke` of data")
    So_luong_merchant_qr_diem = serializers.FloatField(help_text="`So_luong_merchant_qr_diem` of data")
    Doanh_so_thanh_toan_pos_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Doanh_so_thanh_toan_pos_ty_le_htkh_luy_ke` of data")
    Doanh_so_thanh_toan_pos_diem = serializers.FloatField(help_text="`Doanh_so_thanh_toan_pos_diem` of data")
    Loi_nhuan_truoc_thue_ty_le_ktkh_luy_ke = serializers.CharField(help_text="`Loi_nhuan_truoc_thue_ty_le_ktkh_luy_ke` of data")
    Loi_nhuan_truoc_thue_diem = serializers.FloatField(help_text="`Loi_nhuan_truoc_thue_diem` of data")
    So_luong_khach_hang_moi_ty_le_htkh_luy_ke = serializers.CharField(help_text="`So_luong_khach_hang_moi_ty_le_htkh_luy_ke` of data")
    So_luong_khach_hang_moi_diem = serializers.FloatField(help_text="`So_luong_khach_hang_moi_diem` of data")
    So_luong_hop_dong_ebanking_ty_le_htkh_luy_ke = serializers.CharField(help_text="`So_luong_hop_dong_ebanking_ty_le_htkh_luy_ke` of data")
    So_luong_hop_dong_ebanking_diem = serializers.FloatField(help_text="`So_luong_hop_dong_ebanking_diem` of data")
    So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_ty_le_ktkh_luy_ke = serializers.CharField(help_text="`So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_ty_le_ktkh_luy_ke` of data")
    So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_diem = serializers.FloatField(help_text="`So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_diem` of data")
    Doanh_so_bao_lanh_ty_le_htkh_luy_ke = serializers.CharField(help_text="`Doanh_so_bao_lanh_ty_le_htkh_luy_ke` of data")
    Doanh_so_bao_lanh_diem = serializers.FloatField(help_text="`Doanh_so_bao_lanh_diem` of data")
















