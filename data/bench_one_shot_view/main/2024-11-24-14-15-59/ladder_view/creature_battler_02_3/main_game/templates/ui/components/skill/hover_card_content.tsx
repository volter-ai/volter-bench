import * as React from "react"
import { HoverCardContent as HoverCardContentPrimitive } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillHoverCardContentProps extends React.ComponentProps<typeof HoverCardContentPrimitive> {
  uid: string
}

let SkillHoverCardContentBase = React.forwardRef<
  React.ElementRef<typeof HoverCardContentPrimitive>,
  SkillHoverCardContentProps
>((props, ref) => (
  <HoverCardContentPrimitive ref={ref} {...props} />
))

SkillHoverCardContentBase.displayName = "SkillHoverCardContent"

let SkillHoverCardContent = withClickable(SkillHoverCardContentBase)

export { SkillHoverCardContent }
