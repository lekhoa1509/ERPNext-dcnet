<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSpy v2010 rel. 3 (http://www.altova.com) by MESMERiZE (MSM) -->
<xs:schema xmlns="http://kekhaithue.gdt.gov.vn/TKhaiThue" xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://kekhaithue.gdt.gov.vn/TKhaiThue" elementFormDefault="qualified" attributeFormDefault="unqualified">
	<xs:redefine schemaLocation="..\TKhaiThue_DBHC.xsd">
		<xs:complexType name="CTieuTKhaiChinhType">
			<xs:complexContent>
				<xs:extension base="CTieuTKhaiChinhType">
					<xs:sequence>
						<xs:element name="Header">
							<xs:annotation>
								<xs:documentation>Thông tin chung</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="toChucCoQTTTheoUyQuyen" type="xs:boolean">
										<xs:annotation>
											<xs:documentation>Tổ chức có quyết toán thuế theo uỷ quyền của cá nhân được điều chuyển từ tổ chức cũ đến tổ chức mới do tổ chức cũ thực hiện sáp nhập, hợp nhất, chia, tách, chuyển đổi loại hình doanh nghiệp hoặc điều chuyển trong cùng hệ thống</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ma_THQuyetToan" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Trường hợp quyết toán</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ten_THQuyetToan" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Tên trường hợp quyết toán</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="hanNop" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Hạn nộp</xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="NVuKhauTruThue">
							<xs:annotation>
								<xs:documentation>I. NGHĨA VỤ KHẤU TRỪ THUẾ CỦA TỔ CHỨC, CÁ NHÂN TRẢ THU NHẬP  </xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="ct16" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số người lao động:</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct17" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó: Cá nhân cư trú có hợp đồng lao động </xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct18" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số cá nhân đã khấu trừ thuế [18]=[19]+[20]</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct19" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân cư trú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct20" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân không cư trú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct21" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số cá nhân thuộc diện được miễn, giảm thuế theo Hiệp định tránh đánh thuế hai lần</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct22" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số cá nhân giảm trừ gia cảnh</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct23" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng thu nhập chịu thuế trả cho cá nhân [23]=[24]+[25]</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct24" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân cư trú </xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct25" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân không cư trú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct26" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó: Tổng thu nhập chịu thuế từ tiền phí mua bảo hiểm nhân thọ, bảo hiểm không bắt buộc khác của doanh nghiệp bảo hiểm không thành lập tại Việt Nam cho người lao độngtrú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct27" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó tổng thu nhập chịu thuế được miễn theo quy định của Hợp đồng dầu khí</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct28" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng thu nhập chịu thuế trả cho cá nhân thuộc diện phải khấu trừ thuế [28]=[29]+[30]</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct29" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân cư trú </xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct30" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân không cư trú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct31" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế thu nhập cá nhân đã khấu trừ [31]=[32]+[33]</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct32" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân cư trú </xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct33" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Cá nhân không cư trú</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct34" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó: Tổng số thuế thu nhập cá nhân đã khấu trừ trên tiền phí mua bảo hiểm nhân thọ, bảo hiểm không bắt buộc khác của doanh nghiệp bảo hiểm không thành lập tại Việt Nam cho người lao động </xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="NVuQToanThay">
							<xs:annotation>
								<xs:documentation>II. NGHĨA VỤ QUYẾT TOÁN THAY CHO CÁ NHÂN</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="ct35" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số cá nhân uỷ quyền cho tổ chức, cá nhân trả thu nhập quyết toán thay</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct36" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế TNCN đã khấu trừ</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct37" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó: Số thuế thu nhập cá nhân đã khấu trừ tại tổ chức trước khi điều chuyển (trường hợp có đánh dấu vào chỉ tiêu [04])</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct38" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế thu nhập cá nhân  phải nộp</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct39" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế thu nhập cá nhân được miễn do cá nhân có số thuế còn phải nộp sau ủy quyền quyết toán từ 50.000 đồng trở xuống</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct40" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế thu nhập cá nhân còn phải nộp 
[40] = ([38] – [36] – [39]) >0</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct41" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế thu nhập cá nhân đã nộp thừa </xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
		<xs:complexType name="PLucType">
			<xs:complexContent>
				<xs:extension base="PLucType">
					<xs:sequence>
						<xs:element name="PLuc_05_1_BK_QTT" minOccurs="0">
							<xs:annotation>
								<xs:documentation>Phụ lục BẢNG KÊ CHI TIẾT CÁ NHÂN THUỘC DIỆN TÍNH THUẾ THEO BIỂU LŨY TIẾN TỪNG PHẦN</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="BKeCTietCNhan" maxOccurs="unbounded">
										<xs:complexType>
											<xs:sequence>
												<xs:element name="coDieuChinhSoLieu" type="xs:boolean" minOccurs="0">
													<xs:annotation>
														<xs:documentation>Có điều chỉnh số liệu (cập nhật cho ứng dụng HTKK, Tool QTT)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct07" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="nguoiVNSongNN_NguoiNN" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Người việt nam sống ở nước ngoài không có mã định danh và người nước ngoài</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09a_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã loại giấy tờ: cmnd-1010, cccd-2080, hộ chiếu-1020, khac-3000, GKS-5000, khác-3000</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09a_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số CMND/ Hộ chiếu</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct10" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Cá nhân uỷ quyền quyết toán thay</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct11" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Cá nhân nước ngoài uỷ quyền quyết toán dưới 12 tháng/năm</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct13" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: TNCT tại tổ chức trước khi điều chuyển (trường hợp có đánh dấu vào chỉ tiêu [04] tại Tờ khai 05/QTT-TNCN)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct14" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: thu nhập chịu thuế được miễn theo Hiệp định</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct15" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: thu nhập chịu thuế được miễn theo quy định của Hợp đồng dầu khí</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct16" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số lượng NPT tính giảm trừ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct17" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số tiền  giảm trừ gia cảnh</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct18" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Từ thiện, nhân đạo, khuyến học</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct19" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Bảo hiểm được trừ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct20" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Quĩ hưu trí tự nguyện được trừ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct21" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Thu nhập tính thuế ([21]= [12]-[14]-[15]-[17] –[18] –[19]-[20])</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct22" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số thuế TNCN đã khấu trừ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct23" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: số thuế đã khấu trừ tại tổ chức trước khi điều chuyển (trường hợp có đánh dấu vào chỉ tiêu [04] tại Tờ khai 05/QTT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct24" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số thuế phải nộp</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct25" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số thuế đã nộp thừa</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct26" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số thuế còn phải nộp</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct27" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>  Cá nhân có số thuế được miễn do có số thuế còn phải nộp từ 50.000 đồng trở xuống</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
											<xs:attribute name="id" type="xs:string"/>
										</xs:complexType>
									</xs:element>
									<xs:element name="ct28" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng thu nhập chịu thuế</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct29" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng TNCT tại tổ chức trước khi điều chuyển (trường hợp có đánh dấu vào chỉ tiêu [04] tại Tờ khai 05/QTT-TNCN)</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct30" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Theo Hiệp định</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct31" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tỏng theo quy định của Hợp đồng dầu khí</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct32" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Số lượng NPT tính giảm trừ</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct33" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số tiền  giảm trừ gia cảnh</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct34" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Từ thiện, nhân đạo, khuyến học</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct35" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Bảo hiểm được trừ</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct36" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Quĩ hưu trí tự nguyện được trừ</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct37" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Thu nhập tính thuế</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct38" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Số thuế TNCN đã khấu trừ</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct39" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số thuế đã khấu trừ tại tổ chức trước khi điều chuyển (trường hợp có đánh dấu vào chỉ tiêu [04] tại Tờ khai 05/QTT</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct40" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Tổng số thuế phải nộp</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct41" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Số thuế đã nộp thừa</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct42" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Số thuế còn phải nộp</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct43" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng cá nhân có số thuế được miễn</xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="PLuc_05_2_BK_QTT" minOccurs="0">
							<xs:annotation>
								<xs:documentation>Phụ lục BẢNG KÊ CHI TIẾT CÁ NHÂN THUỘC DIỆN TÍNH THUẾ THEO THUẾ SUẤT TOÀN PHẦN</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="BKeCTietCNhan" maxOccurs="unbounded">
										<xs:complexType>
											<xs:sequence>
												<xs:element name="coDieuChinhSoLieu" type="xs:boolean" minOccurs="0">
													<xs:annotation>
														<xs:documentation>Có điều chỉnh số liệu (cập nhật cho ứng dụng HTKK, Tool QTT)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct07" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="nguoiVNSongNN_NguoiNN" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Người việt nam sống ở nước ngoài không có mã định danh và người nước ngoài</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09a_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã loại giấy tờ: cmnd-1080, cccd-2080, hộ chiếu-1020, khac-3000</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09a_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số CMND/
Hộ chiếu
</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct10" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Cá nhân không cư trú</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct11" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: TNCT từ phí mua BH nhân thọ, BH không bắt buộc khác của DN BH không thành lập tại Việt Nam cho người lao động</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct13" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó thu nhập chịu thuế được miễn theo Hiệp định </xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct14" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Theo quy định của Hợp đồng dầu khí</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct15" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Tổng số</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct16" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Trong đó: Số thuế từ phí mua BH nhân thọ, BH không bắt buộc khác của DN BH không thành lập tại Việt Nam cho người lao động</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
											<xs:attribute name="id" type="xs:string"/>
										</xs:complexType>
									</xs:element>
									<xs:element name="ct17" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct18" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng Trong đó: TNCT từ phí mua BH nhân thọ, BH không bắt buộc khác của DN BH không thành lập tại Việt Nam cho người lao động</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct19" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng theo hiệp định</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct20" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng theo dầu khí</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct21" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Tổng số</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ct22" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Trong đó: Số thuế từ phí mua BH nhân thọ, BH không bắt buộc khác của DN BH không thành lập tại Việt Nam cho người lao động</xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="PLuc_05_3_BK_QTT" minOccurs="0">
							<xs:annotation>
								<xs:documentation>Phụ lục BẢNG KÊ THÔNG TIN NGƯỜI PHỤ THUỘC GIẢM TRỪ GIA CẢNH </xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="BKeTTinNPT" maxOccurs="unbounded">
										<xs:complexType>
											<xs:sequence>
												<xs:element name="ct07" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>MST của người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên người phụ thuộc</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct10" type="xs:date" nillable="true">
													<xs:annotation>
														<xs:documentation>Ngày sinh người phụ thuộc</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct11" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>MST của người phụ thuộc</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="nguoiVNSongNN_NguoiNN" type="xs:boolean" nillable="true">
													<xs:annotation>
														<xs:documentation>Người việt nam sống ở nước ngoài không có mã định danh và người nước ngoài</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã loại giấy tờ: cmnd-1080, cccd-2080, hộ chiếu-1020, khac-3000</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct13" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct14_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã Quan hệ với người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct14_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên Quan hệ với người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct15" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Từ tháng</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct16" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Đến tháng</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
											<xs:attribute name="id" type="xs:string"/>
										</xs:complexType>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="PL01_KHBS" minOccurs="0">
							<xs:complexType>
								<xs:sequence>
									<xs:element name="Header">
										<xs:annotation>
											<xs:documentation>Thông tin chung</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="maTKhai" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã tờ khai</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenTKhai" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên tờ khai</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="maGiaoDich" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã giao dịch điện tử</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="KyKKhaiThue">
													<xs:annotation>
														<xs:documentation>Kỳ kê khai thuế</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="kieuKy">
																<xs:annotation>
																	<xs:documentation>Kiểu kỳ</xs:documentation>
																</xs:annotation>
																<xs:simpleType>
																	<xs:restriction base="xs:string">
																		<xs:pattern value="D|M|Y|K|Q"/>
																	</xs:restriction>
																</xs:simpleType>
															</xs:element>
															<xs:element name="kyKKhai" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Quý: Q/YYYY, ngày: DD/MM/YYYY, tháng: MM/YYYY, năm: YYYY, Kỳ: K/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiTuNgay" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng DD/MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiDenNgay" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng DD/MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiTuThang" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiDenThang" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
												<xs:element name="soLan" type="xs:nonNegativeInteger">
													<xs:annotation>
														<xs:documentation>Số lần</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="mst" type="TINType">
													<xs:annotation>
														<xs:documentation>Mã số thuế NNT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenNNT" type="xs:token">
													<xs:annotation>
														<xs:documentation>Tên NNT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="mstDLyThue" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenDLyThue" type="xs:token" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="soHDongDLyThue" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số hợp đồng đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ngayKyHDDLyThue" type="xs:date" nillable="true">
													<xs:annotation>
														<xs:documentation>Ngày ký hợp đồng</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
									<xs:element name="ma_DonViTien" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Mã đơn vị tiền</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ten_DonViTien" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Tên đơn vị tiền</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="Muc_A">
										<xs:annotation>
											<xs:documentation>A. Xác định tăng/giảm số thuế phải nộp và tiền chậm nộp, tăng/giảm số thuế được khấu trừ, tăng/giảm số thuế đề nghị hoàn</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="Muc_I">
													<xs:annotation>
														<xs:documentation>I. Xác định tăng/giảm số thuế phải nộp và tiền chậm nộp:</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="Muc_1">
																<xs:annotation>
																	<xs:documentation>1. Số thuế phải nộp trên tờ khai điều chỉnh tăng/giảm</xs:documentation>
																</xs:annotation>
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="ChiTiet" maxOccurs="unbounded">
																			<xs:complexType>
																				<xs:sequence>
																					<xs:element name="ct2_ma" type="xs:string" nillable="true">
																						<xs:annotation>
																							<xs:documentation>Mã tiểu mục</xs:documentation>
																						</xs:annotation>
																					</xs:element>
																					<xs:element name="ct2_ten" type="xs:string" nillable="true">
																						<xs:annotation>
																							<xs:documentation>Tên tiểu mục</xs:documentation>
																						</xs:annotation>
																					</xs:element>
																					<xs:element name="ct3" type="xs:long" nillable="true">
																						<xs:annotation>
																							<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																						</xs:annotation>
																					</xs:element>
																				</xs:sequence>
																				<xs:attribute name="id" type="xs:string" use="required"/>
																			</xs:complexType>
																		</xs:element>
																		<xs:element name="tongCong_ct10" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																	</xs:sequence>
																</xs:complexType>
															</xs:element>
															<xs:element name="Muc_2">
																<xs:annotation>
																	<xs:documentation>2. Số thuế phải nộp trên Phụ lục phân bổ điều chỉnh tăng/giảm</xs:documentation>
																</xs:annotation>
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="DSachPLuc">
																			<xs:complexType>
																				<xs:sequence>
																					<xs:element name="BKePLuc" maxOccurs="unbounded">
																						<xs:complexType>
																							<xs:sequence>
																								<xs:element name="ma_PLuc" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Mã phụ lục</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ten_PLuc" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Tên phụ lục</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="CTietPLuc">
																									<xs:complexType>
																										<xs:sequence>
																											<xs:element name="ChiTiet" minOccurs="0" maxOccurs="unbounded">
																												<xs:complexType>
																													<xs:sequence>
																														<xs:element name="ct2_ma" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Mã đơn vị phụ thuộc, địa điểm kinh doanh/tên mặt hàng/tỉnh nơi không có đơn vị phụ thuộc/địa điểm kinh doanh/đơn vị tiêu thụ/cơ sở khai thác></xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct2_ten" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Tên đơn vị phụ thuộc, địa điểm kinh doanh/tên mặt hàng/tỉnh nơi không có đơn vị phụ thuộc/địa điểm kinh doanh/đơn vị tiêu thụ/cơ sở khai thác</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct3_ma" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Mã số thuế/mã số địa điểm kinh doanh (nếu có)</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct3_ten" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Tên Mã số thuế/mã số địa điểm kinh doanh (nếu có)</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct04_ma" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Mã huyện</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct04_ten" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Tên huyện</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct05_ma" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Mã tỉnh</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct05_ten" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Tên tỉnh</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct06_ma" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Mã cơ quan thuế quản lý địa bàn nhận phân bổ</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct06_ten" type="xs:string" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Tên cơ quan thuế quản lý địa bàn nhận phân bổ</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																														<xs:element name="ct7" type="xs:long" nillable="true">
																															<xs:annotation>
																																<xs:documentation>Số tiền thuế phải nộp điều chỉnh tăng/ giảm (tăng ghi (+), giảm ghi (-))</xs:documentation>
																															</xs:annotation>
																														</xs:element>
																													</xs:sequence>
																													<xs:attribute name="id" type="xs:string" use="required"/>
																												</xs:complexType>
																											</xs:element>
																										</xs:sequence>
																									</xs:complexType>
																								</xs:element>
																							</xs:sequence>
																							<xs:attribute name="id" type="xs:string" use="required"/>
																						</xs:complexType>
																					</xs:element>
																					<xs:element name="tongCong_ct11" type="xs:long" nillable="true">
																						<xs:annotation>
																							<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																						</xs:annotation>
																					</xs:element>
																				</xs:sequence>
																			</xs:complexType>
																		</xs:element>
																	</xs:sequence>
																</xs:complexType>
															</xs:element>
															<xs:element name="Muc_3">
																<xs:annotation>
																	<xs:documentation>3. Xác định số tiền chậm nộp điều chỉnh tăng/giảm (tăng ghi (+), giảm ghi (-)):</xs:documentation>
																</xs:annotation>
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="ct3a_1" type="xs:date" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Đến ngày</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct3a_2" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Số ngày chậm nộp</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct3b" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Số tiền chậm nộp tăng/giảm</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																	</xs:sequence>
																</xs:complexType>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
												<xs:element name="Muc_II">
													<xs:annotation>
														<xs:documentation>II. Số thuế được khấu trừ điều chỉnh tăng/giảm</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="ChiTiet" maxOccurs="unbounded">
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="ct2_ma" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Mã tiểu mục</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct2_ten" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tên tiểu mục</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct3" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																	</xs:sequence>
																	<xs:attribute name="id" type="xs:string" use="required"/>
																</xs:complexType>
															</xs:element>
															<xs:element name="tongCong_ct12" type="xs:long" nillable="true">
																<xs:annotation>
																	<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
												<xs:element name="Muc_III">
													<xs:annotation>
														<xs:documentation>III. Số thuế đề nghị hoàn điều chỉnh tăng/giảm</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="ChiTiet" maxOccurs="unbounded">
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="ct2_ma" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Mã tiểu mục</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct2_ten" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tên tiểu mục</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ct3" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																	</xs:sequence>
																	<xs:attribute name="id" type="xs:string" use="required"/>
																</xs:complexType>
															</xs:element>
															<xs:element name="tongCong_ct13" type="xs:long" nillable="true">
																<xs:annotation>
																	<xs:documentation>Tăng/giảm số thuế phải nộp (tăng ghi (+), giảm ghi (-))</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
									<xs:element name="Muc_B">
										<xs:annotation>
											<xs:documentation>B. Số thuế thu hồi hoàn và tiền chậm nộp (nếu có):</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="Muc_I">
													<xs:annotation>
														<xs:documentation>I. Số thuế thu hồi hoàn</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="ct_1" type="xs:long" nillable="true">
																<xs:annotation>
																	<xs:documentation>1. Số tiền thu hồi hoàn</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_2_so" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Quyết định hoàn thuế: Số </xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_2_ngay" type="xs:date" nillable="true">
																<xs:annotation>
																	<xs:documentation>Quyết định hoàn thuế: ngày</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_2_CQT_ma" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Quyết định hoàn thuế: CQT ban hành</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_2_CQT_ten" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Quyết định hoàn thuế: CQT ban hành</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_3_so" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Lệnh hoàn thuế: Số </xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_3_ngay" type="xs:date" nillable="true">
																<xs:annotation>
																	<xs:documentation>Lệnh hoàn thuế: Ngày</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
												<xs:element name="Muc_II">
													<xs:annotation>
														<xs:documentation>II. Tiền chậm nộp</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="ct_1" type="xs:long" nillable="true">
																<xs:annotation>
																	<xs:documentation>1. Số ngày nhận được tiền hoàn thuế</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ct_2" type="xs:long" nillable="true">
																<xs:annotation>
																	<xs:documentation>2. Số tiền chậm nộp </xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="PL01_1_KHBS" minOccurs="0">
							<xs:complexType>
								<xs:sequence>
									<xs:element name="Header">
										<xs:annotation>
											<xs:documentation>Thông tin chung</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="maTKhai" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã tờ khai</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenTKhai" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên tờ khai</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="maGiaoDich" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã giao dịch điện tử</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="KyKKhaiThue">
													<xs:annotation>
														<xs:documentation>Kỳ kê khai thuế</xs:documentation>
													</xs:annotation>
													<xs:complexType>
														<xs:sequence>
															<xs:element name="kieuKy">
																<xs:annotation>
																	<xs:documentation>Kiểu kỳ</xs:documentation>
																</xs:annotation>
																<xs:simpleType>
																	<xs:restriction base="xs:string">
																		<xs:pattern value="D|M|Y|K|Q"/>
																	</xs:restriction>
																</xs:simpleType>
															</xs:element>
															<xs:element name="kyKKhai" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Quý: Q/YYYY, ngày: DD/MM/YYYY, tháng: MM/YYYY, năm: YYYY, Kỳ: K/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiTuNgay" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng DD/MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiDenNgay" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng DD/MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiTuThang" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="kyKKhaiDenThang" type="xs:string">
																<xs:annotation>
																	<xs:documentation>Định dạng MM/YYYY</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
												<xs:element name="soLan" type="xs:nonNegativeInteger">
													<xs:annotation>
														<xs:documentation>Số lần</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="mst" type="TINType">
													<xs:annotation>
														<xs:documentation>Mã số thuế NNT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenNNT" type="xs:token">
													<xs:annotation>
														<xs:documentation>Tên NNT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="mstDLyThue" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenDLyThue" type="xs:token" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="soHDongDLyThue" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số hợp đồng đại lý thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ngayKyHDDLyThue" type="xs:date" nillable="true">
													<xs:annotation>
														<xs:documentation>Ngày ký hợp đồng</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
									<xs:element name="ma_DonViTien" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Mã đơn vị tiền</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="ten_DonViTien" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Tên đơn vị tiền</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="Muc_A">
										<xs:annotation>
											<xs:documentation>A. Thông tin khai bổ sung</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="DSachHSo">
													<xs:complexType>
														<xs:sequence>
															<xs:element name="BKeHSo" maxOccurs="unbounded">
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="ma_HSo" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Mã hồ sơ</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="ten_HSo" type="xs:string" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tên hồ sơ</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="CTietHSo">
																			<xs:complexType>
																				<xs:sequence>
																					<xs:element name="ChiTiet" minOccurs="0" maxOccurs="unbounded">
																						<xs:complexType>
																							<xs:sequence>
																								<xs:element name="ct2_ma" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Mã Tên chỉ tiêu 
điều chỉnh/ Tên hàng hóa, dịch vụ</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct2_ten" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Tên Tên chỉ tiêu 
điều chỉnh/ Tên hàng hóa, dịch vụ</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_ma" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Mã số chỉ tiêu</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_ten" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Tên Mã số chỉ tiêu</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_1_ma" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Mã số chỉ tiêu Dành cho đơn vị phụ thuộc/nhà máy...</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_1_ten" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Tên Mã số chỉ tiêu Dành cho đơn vị phụ thuộc/nhà máy...</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_2_ma" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Mã số chỉ tiêu Dành cho đ  những mẫu không có key, nhập dạng text </xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct3_2_ten" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Tên Mã số chỉ tiêu Dành cho  những mẫu không có key, nhập dạng text .</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct04" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Số đã kê khai</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct05" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Số điều chỉnh</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct06" type="xs:decimal" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Chênh lệch/thay đổi giữa số điều chỉnh với số đã kê khai</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct7" type="xs:decimal" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Điều chỉnh tăng/giảm nghĩa vụ thuế</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																								<xs:element name="ct8" type="xs:string" nillable="true">
																									<xs:annotation>
																										<xs:documentation>Lý do</xs:documentation>
																									</xs:annotation>
																								</xs:element>
																							</xs:sequence>
																							<xs:attribute name="id" type="xs:string" use="required"/>
																						</xs:complexType>
																					</xs:element>
																				</xs:sequence>
																			</xs:complexType>
																		</xs:element>
																	</xs:sequence>
																	<xs:attribute name="id" type="xs:string" use="required"/>
																</xs:complexType>
															</xs:element>
															<xs:element name="TongCong">
																<xs:complexType>
																	<xs:sequence>
																		<xs:element name="tongCong_7" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tổng cộng (tăng +, giảm -) phải nộp:</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="tongCong_8" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tổng cộng (tăng +, giảm -) khấu trừ:</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																		<xs:element name="tongCong_9" type="xs:long" nillable="true">
																			<xs:annotation>
																				<xs:documentation>Tổng cộng (tăng +, giảm -) đề nghị hoàn:</xs:documentation>
																			</xs:annotation>
																		</xs:element>
																	</xs:sequence>
																</xs:complexType>
															</xs:element>
														</xs:sequence>
													</xs:complexType>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
									<xs:element name="Muc_B">
										<xs:annotation>
											<xs:documentation>B. Tài liệu kèm theo (nếu có)</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="CTietTaiLieu" maxOccurs="unbounded">
													<xs:complexType>
														<xs:sequence>
															<xs:element name="ma_TLieu" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Mã tài liệu</xs:documentation>
																</xs:annotation>
															</xs:element>
															<xs:element name="ten_TLieu" type="xs:string" nillable="true">
																<xs:annotation>
																	<xs:documentation>Tên tài liệu</xs:documentation>
																</xs:annotation>
															</xs:element>
														</xs:sequence>
														<xs:attribute name="id" type="xs:string" use="required"/>
													</xs:complexType>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:redefine>
</xs:schema>
