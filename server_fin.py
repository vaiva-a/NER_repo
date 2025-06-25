from fastapi import FastAPI, Body
from pydantic import BaseModel
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast, DistilBertForTokenClassification,
    Trainer, TrainingArguments, DataCollatorForTokenClassification
)
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import torch

# Load fine-tuned DistilBERT model and tokenizer
model_path = r"C:/Users/soura/Desktop/PersonalStuff/FinalViva/Project/PROJECT MODEL/fin-ner (3)"  # Update as needed
model = DistilBertForTokenClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model.eval()

# Extract label mappings from the model config
id2label = model.config.id2label
label2id = model.config.label2id

# Initialize FastAPI app
app = FastAPI()
consolidated_tags = {
    # Acquisition and Business Combination Tags
    "BusinessAcquisitionPercentageOfVotingInterestsAcquired": "ACQUISITION",
    "BusinessCombinationAcquisitionRelatedCosts": "ACQUISITION",
    "BusinessCombinationConsiderationTransferred1": "ACQUISITION",
    "BusinessCombinationContingentConsiderationLiability": "ACQUISITION",
    "BusinessAcquisitionEquityInterestsIssuedOrIssuableNumberOfSharesIssued": "ACQUISITION",
    "BusinessCombinationRecognizedIdentifiableAssetsAcquiredAndLiabilitiesAssumedIntangibleAssetsOtherThanGoodwill": "ACQUISITION",
    "BusinessCombinationRecognizedIdentifiableAssetsAcquiredAndLiabilitiesAssumedIntangibles": "ACQUISITION",
    "PaymentsToAcquireBusinessesGross": "ACQUISITION",
    "PaymentsToAcquireBusinessesNetOfCashAcquired": "ACQUISITION",
    "DisposalGroupIncludingDiscontinuedOperationConsideration": "ACQUISITION",
    
    # Debt and Financing Tags
    "DebtInstrumentBasisSpreadOnVariableRate1": "DEBT",
    "DebtInstrumentCarryingAmount": "DEBT",
    "DebtInstrumentFaceAmount": "DEBT",
    "DebtInstrumentFairValue": "DEBT",
    "DebtInstrumentInterestRateEffectivePercentage": "DEBT",
    "DebtInstrumentInterestRateStatedPercentage": "DEBT",
    "DebtInstrumentMaturityDate": "DEBT",
    "DebtInstrumentRedemptionPricePercentage": "DEBT",
    "DebtInstrumentTerm": "DEBT",
    "DebtInstrumentUnamortizedDiscount": "DEBT",
    "DebtWeightedAverageInterestRate": "DEBT",
    "AmortizationOfFinancingCosts": "DEBT",
    "DeferredFinanceCostsGross": "DEBT",
    "DeferredFinanceCostsNet": "DEBT",
    "LongTermDebt": "DEBT",
    "LongTermDebtFairValue": "DEBT",
    "RepaymentsOfDebt": "DEBT",
    "LineOfCredit": "DEBT",
    "LineOfCreditFacilityCommitmentFeePercentage": "DEBT",
    "LineOfCreditFacilityCurrentBorrowingCapacity": "DEBT",
    "LineOfCreditFacilityInterestRateAtPeriodEnd": "DEBT",
    "LineOfCreditFacilityMaximumBorrowingCapacity": "DEBT",
    "LineOfCreditFacilityRemainingBorrowingCapacity": "DEBT",
    "LineOfCreditFacilityUnusedCapacityCommitmentFeePercentage": "DEBT",
    "InterestExpense": "DEBT",
    "InterestExpenseDebt": "DEBT",
    "GainsLossesOnExtinguishmentOfDebt": "DEBT",
    
    # Equity and Stock Tags
    "CommonStockCapitalSharesReservedForFutureIssuance": "EQUITY",
    "CommonStockDividendsPerShareDeclared": "EQUITY",
    "CommonStockParOrStatedValuePerShare": "EQUITY",
    "CommonStockSharesAuthorized": "EQUITY",
    "CommonStockSharesOutstanding": "EQUITY",
    "PreferredStockDividendRatePercentage": "EQUITY",
    "PreferredStockSharesAuthorized": "EQUITY",
    "ClassOfWarrantOrRightExercisePriceOfWarrantsOrRights1": "EQUITY",
    "ProceedsFromIssuanceOfCommonStock": "EQUITY",
    "SharePrice": "EQUITY",
    "SaleOfStockNumberOfSharesIssuedInTransaction": "EQUITY",
    "SaleOfStockPricePerShare": "EQUITY",
    "StockIssuedDuringPeriodSharesNewIssues": "EQUITY",
    "StockRepurchaseProgramAuthorizedAmount1": "EQUITY",
    "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1": "EQUITY",
    "StockRepurchasedAndRetiredDuringPeriodShares": "EQUITY",
    "StockRepurchasedDuringPeriodShares": "EQUITY",
    "TreasuryStockAcquiredAverageCostPerShare": "EQUITY",
    "TreasuryStockSharesAcquired": "EQUITY",
    "TreasuryStockValueAcquiredCostMethod": "EQUITY",
    
    # Compensation and Benefits Tags
    "AllocatedShareBasedCompensationExpense": "COMPENSATION",
    "EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized": "COMPENSATION",
    "EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognizedPeriodForRecognition1": "COMPENSATION",
    "EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognizedShareBasedAwardsOtherThanOptions": "COMPENSATION",
    "EmployeeServiceShareBasedCompensationTaxBenefitFromCompensationExpense": "COMPENSATION",
    "ShareBasedCompensation": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardAwardVestingPeriod1": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriod": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriodWeightedAverageGrantDateFairValue": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsNonvestedNumber": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsVestedInPeriodTotalFairValue": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardNumberOfSharesAuthorized": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardNumberOfSharesAvailableForGrant": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsExercisesInPeriodTotalIntrinsicValue": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsGrantsInPeriodGross": "COMPENSATION",
    "ShareBasedCompensationArrangementByShareBasedPaymentAwardOptionsGrantsInPeriodWeightedAverageGrantDateFairValue": "COMPENSATION",
    "SharebasedCompensationArrangementBySharebasedPaymentAwardAwardVestingRightsPercentage": "COMPENSATION",
    "SharebasedCompensationArrangementBySharebasedPaymentAwardExpirationPeriod": "COMPENSATION",
    "DefinedBenefitPlanContributionsByEmployer": "COMPENSATION",
    "DefinedContributionPlanCostRecognized": "COMPENSATION",
    
    # Revenue and Customer Contracts Tags
    "ContractWithCustomerLiability": "REVENUE",
    "ContractWithCustomerLiabilityRevenueRecognized": "REVENUE",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "REVENUE",
    "RevenueFromContractWithCustomerIncludingAssessedTax": "REVENUE",
    "RevenueRemainingPerformanceObligation": "REVENUE",
    "RevenueFromRelatedParties": "REVENUE",
    "Revenues": "REVENUE",
    "CapitalizedContractCostAmortization": "REVENUE",
    
    # Assets and Intangibles Tags
    "AmortizationOfIntangibleAssets": "ASSETS",
    "AcquiredFiniteLivedIntangibleAssetsWeightedAverageUsefulLife": "ASSETS",
    "FiniteLivedIntangibleAssetUsefulLife": "ASSETS",
    "Goodwill": "ASSETS",
    "GoodwillImpairmentLoss": "ASSETS",
    "AssetImpairmentCharges": "ASSETS",
    "CashAndCashEquivalentsFairValueDisclosure": "ASSETS",
    "Depreciation": "ASSETS",
    "PropertyPlantAndEquipmentUsefulLife": "ASSETS",
    
    # Leases and Property Tags
    "OperatingLeaseCost": "LEASES",
    "OperatingLeaseExpense": "LEASES",
    "OperatingLeaseLiability": "LEASES",
    "OperatingLeasePayments": "LEASES",
    "OperatingLeaseRightOfUseAsset": "LEASES",
    "OperatingLeaseWeightedAverageDiscountRatePercent": "LEASES",
    "OperatingLeaseWeightedAverageRemainingLeaseTerm1": "LEASES",
    "OperatingLeasesRentExpenseNet": "LEASES",
    "LeaseAndRentalExpense": "LEASES",
    "LesseeOperatingLeaseRenewalTerm": "LEASES",
    "LesseeOperatingLeaseTermOfContract": "LEASES",
    "AreaOfRealEstateProperty": "LEASES",
    "NumberOfRealEstateProperties": "LEASES",
    
    # Tax Tags
    "EffectiveIncomeTaxRateContinuingOperations": "TAX",
    "EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate": "TAX",
    "IncomeTaxExpenseBenefit": "TAX",
    "UnrecognizedTaxBenefits": "TAX",
    "UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate": "TAX",
    "OperatingLossCarryforwards": "TAX",
    
    # Investment Tags
    "EquityMethodInvestmentOwnershipPercentage": "INVESTMENT",
    "EquityMethodInvestments": "INVESTMENT",
    "IncomeLossFromEquityMethodInvestments": "INVESTMENT",
    "MinorityInterestOwnershipPercentageByNoncontrollingOwners": "INVESTMENT",
    "MinorityInterestOwnershipPercentageByParent": "INVESTMENT",
    
    # Risk and Contingency Tags
    "AccrualForEnvironmentalLossContingencies": "RISK",
    "LossContingencyAccrualAtCarryingValue": "RISK",
    "LossContingencyDamagesSoughtValue": "RISK",
    "LossContingencyEstimateOfPossibleLoss": "RISK",
    "LossContingencyPendingClaimsNumber": "RISK",
    "GuaranteeObligationsMaximumExposure": "RISK",
    "LettersOfCreditOutstandingAmount": "RISK",
    "DerivativeFixedInterestRate": "RISK",
    "DerivativeNotionalAmount": "RISK",
    "ConcentrationRiskPercentage1": "RISK",
    "RestructuringCharges": "RISK",
    "RestructuringAndRelatedCostExpectedCost1": "RISK",
    "CumulativeEffectOfNewAccountingPrincipleInPeriodOfAdoption": "RISK"
}
# Request format
class ParagraphRequest(BaseModel):
    paragraph: str

@app.get("/")
def home():
    return {"message": "Financial NER API is running"}

@app.post("/predict")
def predict(request: ParagraphRequest):
    """NER prediction using fine-tuned DistilBERT."""
    lines = request.paragraph.split(".")
    allTagData = {}

    for idx, line in enumerate(lines):
        words = line.strip().split()
        if not words:
            continue

        tokens = tokenizer(words, truncation=True, is_split_into_words=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**tokens)
        predictions = torch.argmax(outputs.logits, dim=-1).squeeze().tolist()
        word_ids = tokens.word_ids()

        tagData = {}
        previous_word_idx = None
        for word_idx, pred in zip(word_ids, predictions):
            if word_idx is not None and word_idx != previous_word_idx:
                original_tag = id2label.get(pred, "O")
                
                # Apply consolidated tag mapping while preserving prefix
                if original_tag != "O":
                    # Check if tag has a prefix (B- or I-)
                    if original_tag.startswith("B-") or original_tag.startswith("I-"):
                        prefix = original_tag[:2]  # Get B- or I-
                        tag_name = original_tag[2:]  # Get the actual tag name
                        
                        # Apply consolidated mapping if tag exists in the mapping
                        if tag_name in consolidated_tags:
                            final_tag = prefix + consolidated_tags[tag_name]
                        else:
                            final_tag = original_tag
                    else:
                        # No prefix but still apply consolidated mapping
                        if original_tag in consolidated_tags:
                            final_tag = consolidated_tags[original_tag]
                        else:
                            final_tag = original_tag
                else:
                    final_tag = "O"  # Keep "O" as is
                tagData[word_idx] = {
                    "word": words[word_idx],
                    "tag": final_tag
                }
                previous_word_idx = word_idx

        allTagData[idx] = {
            "sentence_number": idx,
            "annotations": tagData
        }

    return allTagData

# Function to align labels with tokenized words
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples['Words'],
        is_split_into_words=True,
        padding='max_length',
        truncation=True,
    )

    labels = []
    for i, word_list in enumerate(examples['Words']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)
            else:
                label_ids.append(label2id.get(examples['Tags'][i][word_id], -100))
        labels.append(label_ids)

    tokenized_inputs['labels'] = labels
    return tokenized_inputs

# Function to get updated sentences - Modified to match code2's format
def get_updated_sentences(ann, autotaglist):
    updated_sentences = []

    for ini_sentence, fin_sentence in zip(ann, autotaglist):
        annotations_ini = ini_sentence["annotations"]
        annotations_fin = fin_sentence["annotations"]

        modified = False
        words, tags = [], []

        for word, fin_tag in annotations_fin.items():
            ini_tag = annotations_ini.get(word, 'O')
            if fin_tag != ini_tag:
                modified = True
            words.append(word)
            tags.append(fin_tag)

        if modified:
            updated_sentences.append({"Words": words, "Tags": tags})

    return pd.DataFrame(updated_sentences)

@app.post("/learn")
async def update_model_with_incremental_data(ann: list = Body(...), autotaglist: list = Body(...)):
    try:
        # Prepare training data
        incremental_train_data = get_updated_sentences(ann, autotaglist)

        if incremental_train_data.empty:
            return {"message": "No updated data to train on."}

        # Create dataset and tokenize
        incremental_dataset = Dataset.from_pandas(incremental_train_data)
        tokenized_incremental_dataset = incremental_dataset.map(
            tokenize_and_align_labels, batched=True
        )

        # Training arguments with unused columns allowed
        incremental_training_args = TrainingArguments(
            output_dir="./distilbert_incremental",
            learning_rate=3e-5,
            per_device_train_batch_size=8,
            num_train_epochs=1,
            weight_decay=0.01,
            logging_steps=10,
            remove_unused_columns=False
        )

        # Trainer setup
        incremental_trainer = Trainer(
            model=model,
            args=incremental_training_args,
            train_dataset=tokenized_incremental_dataset,
            data_collator=DataCollatorForTokenClassification(tokenizer),
        )

        # Train the model
        incremental_trainer.train()

        # Save the model
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)

        return {"message": "Model updated successfully."}
    except Exception as e:
        return {"message": f"Model update failed: {str(e)}"}