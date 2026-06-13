def generate_report(
        tender1_name,
        tender2_name,
        similarity
        ):
        
        if similarity >= 80:
              
            conclusion = """
            Highly Similar Documents
            """
            recommendation = """
            These tenders have very similar requirements.
            """
              
        elif similarity >= 50:
              
            conclusion = """
            Moderately Similar Documents
            """
            recommendation = """
            Some requirements overlap but significant differences exist.
            """
              
        else:
              
            conclusion = """
            Low Similarity
            """

            recommendation = """
            The tenders appear to be for different purposes.
            """
            
        report = f"""
        Tender Comparison Report
        
        Tender 1:
        {tender1_name}
    
        Tender 2:
        {tender2_name}
        
        Similarity Score:
        {similarity}%
    
        Conclusion:
        {conclusion}
        
        Recommendation:
        {recommendation}
    """
        
        return report