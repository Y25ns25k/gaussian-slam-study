# Portfolio description

## Korean

**정적 3DGS의 gradient 기반 pruning 점수를 Gaussian SLAM으로 옮기는 전이 연구**

학습 중 계산되는 gradient로 Gaussian 중요도(trace)를 매기는 방법을 정적 3DGS에서 검증하고 Gaussian SLAM으로
옮겼습니다. 정적 모델에서는 opacity보다 +1.16 dB(8/8) 좋았지만, SLAM 지도에서는 전역 순위로 지우면 random보다
나빴습니다. 5 cm 복셀별 quota를 도입해 약 24 %를 0.19–0.27 dB 손실로 줄였고(체크포인트 24 % 감소), 같은 조건의
렌더링 기여도 점수와 비교했습니다. 발표된 SLAM 방법은 평가 조건 차이를 명시해 별도로 정리했습니다. 세 진단 실험에서 관측과 판정을 정리하고, 원인 설명은 가설로 남겼습니다. 통계 창 결과는 mixed였고,
불투명 구간에서의 작은 평균을 우위 부재의 증명으로 해석하지 않았습니다. 같은 결과를 유지하는 구현
개선으로 압축 단계를 57.4 % 줄였으며, 데이터·그림 재생성 스크립트와 보고서를 함께 제공합니다.

같은 생성·삭제량을 통제한 별도 온라인 비교에서는 area·trace·random의 영상 품질 수치가 가까웠고, trace의 뚜렷한 추가 이득은 확인하지 못했습니다. 공간 할당과 후속 최적화의 기여는 아직 분리하지 않았습니다.

## English

**Transferring a gradient-based pruning score from static 3DGS to Gaussian SLAM**

The project scores Gaussians by their squared training-loss gradient (trace), validates the score in static 3DGS
(+1.16 dB over opacity at 20 % removal, 8/8 pairs) and moves it into Gaussian-SLAM. Global ranking failed in SLAM maps;
an equal quota per 5 cm voxel removed about 24 % of each saved map for 0.19–0.27 dB, with 24 % smaller checkpoints.
The score is compared against a rendering-contribution control; published SLAM methods are discussed with their evaluation differences. Three diagnostics separated observed composition differences, mixed or unmet threshold outcomes, and
unresolved causal explanations. The window result was mixed; the opacity composition remains a hypothesis. A same-result implementation cut the compression stage by 57.4 %. Data, figure
scripts and the report accompany this study.

A separate online comparison matched births and actual deletions. Area, trace and random produced close image-quality metrics, with no clear additional trace benefit; the roles of spatial allocation and continued mapping remain unresolved.

## Evidence and scope

- [Report](REPORT.md) and [overview](README.md)
- [Cost, quality and failed controls](FOLLOW_UP.md)
- [Runnable numerical helpers](code/README.md)
- [AI assistance and license disclosure](README.md#ai-assistance-and-license)

The descriptions summarize the project. Individual contributions should be described according to the work
actually performed; implementation, execution, review and drafting used the AI assistance disclosed above.
