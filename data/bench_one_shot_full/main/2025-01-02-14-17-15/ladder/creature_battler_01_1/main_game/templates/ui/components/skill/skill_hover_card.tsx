import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import { withClickable } from '@/lib/withClickable'

interface SkillHoverCardProps {
  uid: string
  trigger: React.ReactNode
  content: React.ReactNode
}

let SkillHoverCard: React.FC<SkillHoverCardProps> = ({ uid, trigger, content }) => {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        {trigger}
      </HoverCardTrigger>
      <HoverCardContent>
        {content}
      </HoverCardContent>
    </HoverCard>
  )
}

SkillHoverCard = withClickable(SkillHoverCard)

export { SkillHoverCard }
