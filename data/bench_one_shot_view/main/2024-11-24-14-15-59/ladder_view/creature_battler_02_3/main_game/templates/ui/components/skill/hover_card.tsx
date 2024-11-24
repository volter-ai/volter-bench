import * as React from "react"
import { HoverCard as HoverCardPrimitive } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillHoverCardProps extends React.ComponentProps<typeof HoverCardPrimitive> {
  uid: string
}

let SkillHoverCardBase = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive>,
  SkillHoverCardProps
>((props, ref) => (
  <HoverCardPrimitive ref={ref} {...props} />
))

SkillHoverCardBase.displayName = "SkillHoverCard"

let SkillHoverCard = withClickable(SkillHoverCardBase)

export { SkillHoverCard }
