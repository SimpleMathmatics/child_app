import plotly.express as px


class TimelineUtils:
    @staticmethod
    def create_event_text(df):
        information_list = []
        for i in range(df.shape[0]):
            text_oi = ""
            event_oi = df.EventName.tolist()[i]
            event_info = df.iloc[i].filter(regex=event_oi + "_")
            for j in range(len(event_info)):
                subtext_oi = event_info.keys()[j].replace(event_oi + "_", "") + ": " + str(event_info.iloc[j]) + " <br>"
                text_oi = text_oi + subtext_oi
            information_list.append(text_oi)
        return information_list

    def create_timeline(self, df, childIDs):
        df_oi = df[df.ChildID.isin(childIDs)]
        if df_oi.shape[0] == 0:
            return -1
        event_text = self.create_event_text(df_oi)
        df_oi["Information"] = event_text
        df_oi = df_oi[["ChildID", "TimeWritten", "EventName", "Information"]]

        df_oi["y"] = 0
        df_oi["size"] = 10
        fig = px.scatter(df_oi, x="TimeWritten", y="y", color="EventName", size="size", height=300,
                         hover_name="EventName",
                         hover_data={"Information": True,
                                     "size": False,
                                     "y": False})
        fig.update_layout(yaxis_visible=False, yaxis_showticklabels=True)
        fig.update_layout(xaxis_visible=True, xaxis_showticklabels=False)
        fig.update_xaxes(title="", visible=True, showticklabels=True)
        fig.update_layout({
            "plot_bgcolor": 'rgba(0, 0, 0, 0)',
            "paper_bgcolor": 'rgba(0, 0, 0, 0)',
        })
        fig.update_layout(hovermode='x')
        fig.update_layout(width=1000, height=500)
        fig.add_hline(y=0)
        return fig

    def add_childid_colum(self, df):
        # select only columns that contain the ChildID
        id_df = df.filter(regex="_ChildID$", axis=1)

        # apply the function below, to extract the child ID in each row
        childIDs = id_df.apply(self.get_childid_from_row, axis=1)

        # add the column to the original df
        df.insert(0, "ChildID", childIDs)
        return df

    @staticmethod
    def get_childid_from_row(row):
        row = row.tolist()
        non_nan_count = sum([val != None for val in row])
        if non_nan_count == 0:
            return None
        elif non_nan_count == 1:
            for val in row:
                if val != None:
                    return val
        else:
            raise ValueError("The row contains more than one child ID")
