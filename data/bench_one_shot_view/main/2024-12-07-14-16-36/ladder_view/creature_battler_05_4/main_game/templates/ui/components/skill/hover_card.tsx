import * as React from "react"
import { HoverCard as BaseHoverCard, HoverCardContent as BaseHoverCardContent, HoverCardTrigger as BaseHoverCardTrigger } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface WithUid {
  uid: string
}

let HoverCard = withClickable(BaseHoverCard)
let HoverCardTrigger = withClickable(BaseHoverCardTrigger)
let HoverCardContent = withClickable(BaseHoverCardContent)

export { HoverCard, HoverCardTrigger, HoverCardContent }
