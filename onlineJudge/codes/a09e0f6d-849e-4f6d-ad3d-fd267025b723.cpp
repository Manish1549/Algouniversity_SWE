#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(NULL) {}
};

ListNode* createLinkedList(vector<int>& arr) {
    ListNode* dummy = new ListNode(0);
    ListNode* curr = dummy;
    for (int num : arr) {
        curr->next = new ListNode(num);
        curr = curr->next;
    }
    return dummy->next;
}

void printLinkedList(ListNode* head) {
    while (head) {
        cout << head->val << " ";
        head = head->next;
    }
    cout << endl;
}

ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;

    while (list1 && list2) {
        if (list1->val < list2->val) {
            tail->next = list1;
            list1 = list1->next;
        } else {
            tail->next = list2;
            list2 = list2->next;
        }
        tail = tail->next;
    }

    tail->next = list1 ? list1 : list2;
    return dummy.next;
}

int main() {
    cout << "Enter first sorted list (-1 to end): ";
    vector<int> arr1;
    int num;
    while (cin >> num && num != -1) {
        arr1.push_back(num);
    }

    cout << "Enter second sorted list (-1 to end): ";
    vector<int> arr2;
    while (cin >> num && num != -1) {
        arr2.push_back(num);
    }

    ListNode* l1 = createLinkedList(arr1);
    ListNode* l2 = createLinkedList(arr2);

    ListNode* merged = mergeTwoLists(l1, l2);

    cout << "Merged Sorted List: ";
    printLinkedList(merged);

    return 0;
}
