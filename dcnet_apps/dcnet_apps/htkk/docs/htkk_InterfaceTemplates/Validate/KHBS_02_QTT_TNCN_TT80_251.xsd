<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSpy v2010 rel. 3 (http://www.altova.com) by MESMERiZE (MSM) -->
<xs:schema xmlns="http://kekhaithue.gdt.gov.vn/TKhaiThue" xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://kekhaithue.gdt.gov.vn/TKhaiThue" elementFormDefault="qualified" attributeFormDefault="unqualified">
	<xs:redefine schemaLocation="../TKhaiThue.xsd">
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
									<xs:element name="qTTTheoHSGiamThue" type="xs:boolean">
										<xs:annotation>
											<xs:documentation>Tờ khai quyết toán thuế kèm theo hồ sơ giảm thuế do thiên tai, hoả hoạn, tai nạn, bệnh hiểm nghèo</xs:documentation>
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
									<xs:element name="MST" type="TINType" nillable="true">
										<xs:annotation>
											<xs:documentation>Mã số thuế tổ chức chi trả</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="tenTCCT" type="xs:string" nillable="true">
										<xs:annotation>
											<xs:documentation>Tên tổ chức chi trả</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="dchiTCCT" type="xs:string">
										<xs:annotation>
											<xs:documentation>Địa chỉ tổ chức chi trả thu nhập</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="maHuyenTCCT" type="xs:string">
										<xs:annotation>
											<xs:documentation>Mã huyện</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="tenHuyenTCCT" type="xs:string">
										<xs:annotation>
											<xs:documentation>Tên huyện</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="maTinhTCCT" type="xs:string">
										<xs:annotation>
											<xs:documentation>Mã tỉnh</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="tenTinhTCCT" type="xs:string">
										<xs:annotation>
											<xs:documentation>Tên tỉnh</xs:documentation>
										</xs:annotation>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="ct20" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng thu nhập chịu thuế (TNCT) trong kỳ [20]=[21]+[23]</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct21" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng TNCT phát sinh tại Việt Nam </xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct22" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Trong đó tổng TNCT phát sinh tại Việt Nam được miễn giảm theo Hiệp định (nếu có)</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct23" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng TNCT phát sinh ngoài Việt Nam</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct24" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Số người phụ thuộc</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct25" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Các khoản giảm trừ ([25]=[26]+[27]+[28]+[29]+[30])</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct26" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>a. Cho bản thân</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct27" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>b. Cho những người phụ thuộc được giảm trừ</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct28" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>c. Từ thiện nhân đạo khuyến học</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct29" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>d. Các khoản đóng bảo hiểm được trừ</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct30" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>e. Khoản đóng quỹ hưu trí tự nguyện được trừ</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct31" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng thu nhập tính thuế ([31]=[20]-[22]-[25])</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct32" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế thu nhập cá nhân (TNCN) phát sinh trong kỳ</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct33" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế đã nộp trong  kỳ  
([33]=[34]+[35]+[36]-[37]-[38])</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct34" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>a. Số thuế đã khấu trừ tại tổ chức trả thu nhập</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct35" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>b. Số thuế đã nộp trong năm không qua tổ chức trả thu nhập</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct36" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>c. Số thuế đã nộp ở nước ngoài được trừ (nếu có)</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct37" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>d. Số thuế đã khấu trừ, đã nộp ở nước ngoài trùng do quyết toán vắt năm</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct38" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Số thuế đã nộp trong năm không qua tổ chức trả thu nhập trùng do quyết toán vắt năm </xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct39" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế TNCN được giảm trong kỳ [39]=[40]+[41]</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct40" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>a. Số thuế phải nộp trùng do quyết toán vắt năm</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct41" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>b. Tổng số thuế TNCN được giảm khác </xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct42" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế còn phải nộp trong kỳ 
[42]=([32]-[33]-[39])>0</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct43" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Số thuế được miễn do cá nhân có số tiền thuế phải nộp sau quyết toán từ 50.000 đồng trở xuống </xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct44" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế nộp thừa trong kỳ</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct45" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế đề nghị hoàn trả [45]=[46]+[47]</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct46" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Số thuế hoàn trả cho người nộp thuế</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct47" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Số thuế bù trừ cho khoản phải nộp ngân sách nhà nước khác</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="ct48" type="xs:long" nillable="true">
							<xs:annotation>
								<xs:documentation>Tổng số thuế bù trừ cho các phát sinh của kỳ sau [48]=[44]-[45]</xs:documentation>
							</xs:annotation>
						</xs:element>
						<xs:element name="TTinHoanThue">
							<xs:annotation>
								<xs:documentation>Thông tin hoàn thuế</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="soTienHoanTra" type="xs:long" nillable="true">
										<xs:annotation>
											<xs:documentation>Số tiền hoàn trả: Bằng số</xs:documentation>
										</xs:annotation>
									</xs:element>
									<xs:element name="HinhThucHoanTra">
										<xs:annotation>
											<xs:documentation>Hình thưc hoàn trả</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="chuyenKhoan" type="xs:boolean">
													<xs:annotation>
														<xs:documentation>Chuyển khoản</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenChuTaiKhoan" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên chủ tài khoản</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="soTaiKhoan" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số tài khoản</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenNganHang" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tại Ngân hàng/KBNN</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tienMat" type="xs:boolean">
													<xs:annotation>
														<xs:documentation>Tiền mặt</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenNguoiNhan" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên người nhận tiền</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="maLoaiGiayTo" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="tenLoaiGiayTo" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="soGiayTo" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số giấy tờ:................................................................</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ngayCap" type="xs:date" nillable="true">
													<xs:annotation>
														<xs:documentation>Ngày cấp:.......................... </xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="noiCap" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Truyền tên Tỉnh/Thành Phố hoặc tên quốc gia đối với loại giấy tờ là CMND hoặc Hộ chiếu, CCCD; Hoặc nơi cấp là dạng text</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="noNhanTien" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>nơi nhận tiền hoàn thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
								</xs:sequence>
							</xs:complexType>
						</xs:element>
						<xs:element name="TTinBuTru">
							<xs:annotation>
								<xs:documentation>Đề nghị bù trừ</xs:documentation>
							</xs:annotation>
							<xs:complexType>
								<xs:sequence>
									<xs:element name="TTinKhoanNoKhoanThuPS" maxOccurs="unbounded">
										<xs:complexType>
											<xs:sequence>
												<xs:element name="ct02" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>MST của NNT khác (nếu có)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct03" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên NNT khác (nếu có)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct04" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã định danh khoản phải nộp (ID) (nếu có)</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct05" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Nội dung khoản   nợ/phát sinh</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct06_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã chương</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct06_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên chương</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct07_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã Tiểu mục</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct07_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên Tiểu mục</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã CQT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên CQT</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã địa bàn hành chính</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct09_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>tên địa bàn hành chính</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct10" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Hạn nộp</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct11" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số tiền còn phải nộp </xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số tiền còn phải nộp đề nghị bù trừ với số tiền nộp thừa </xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct13" type="xs:long" nillable="true">
													<xs:annotation>
														<xs:documentation>Số tiền còn phải nộp sau bù trừ</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
											<xs:attribute name="id" type="xs:string"/>
										</xs:complexType>
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
						<xs:element name="PLuc_02_1_BK_QTT_TNCN" minOccurs="0">
							<xs:complexType>
								<xs:sequence>
									<xs:element name="Header">
										<xs:annotation>
											<xs:documentation>Thông tin chung</xs:documentation>
										</xs:annotation>
										<xs:complexType>
											<xs:sequence>
												<xs:element name="ct06" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên vợ (chồng) nếu có</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct07" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct08" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số CMND/ Số hộ chiếu vợ (chồng)</xs:documentation>
													</xs:annotation>
												</xs:element>
											</xs:sequence>
										</xs:complexType>
									</xs:element>
									<xs:element name="CTiet" maxOccurs="unbounded">
										<xs:complexType>
											<xs:sequence>
												<xs:element name="ct10" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Họ và tên</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct11" type="TINType" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã số thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã loại giấy tờ: cmnd=1010;  cccd=2080, hộ chiếu=1020; GKS=5000, khác=3000</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct12_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>tên loại giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct13" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Số giấy tờ</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct14" type="xs:date" nillable="true">
													<xs:annotation>
														<xs:documentation>Ngày sinh</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct15_ma" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Mã Quan hệ với người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct15_ten" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Tên Quan hệ với người nộp thuế</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct16" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Thời gian được tính giảm trừ trong năm - Từ tháng</xs:documentation>
													</xs:annotation>
												</xs:element>
												<xs:element name="ct17" type="xs:string" nillable="true">
													<xs:annotation>
														<xs:documentation>Thời gian được tính giảm trừ trong năm - Đến tháng</xs:documentation>
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
																		<xs:element name="tongCong_7" type="xs:decimal" nillable="true">
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
