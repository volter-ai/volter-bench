import * as React from "react"
import { HoverCardTrigger as HoverCardTriggerPrimitive } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillHoverCardTriggerProps extends React.ComponentProps<typeof HoverCardTriggerPrimitive> {
  uid: string
}

let SkillHoverCardTriggerBase = React.forwardRef<
  React.ElementRef<typeof HoverCardTriggerPrimitive>,
  SkillHoverCardTriggerProps
>((props, ref) => (
  <HoverCardTriggerPrimitive ref={ref} {...props} />
))

SkillHoverCardTriggerBase.displayName = "SkillHoverCardTrigger"

let SkillHoverCardTrigger = withClickable(SkillHoverCardTriggerBase)

export { SkillHoverCardTrigger }
