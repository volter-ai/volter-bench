import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCard> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => (
  <HoverCard {...props}>
    <HoverCardTrigger asChild>
      <button className="px-4 py-2 bg-blue-500 text-white rounded-md">
        {skillName}
      </button>
    </HoverCardTrigger>
    <HoverCardContent>
      <div className="text-sm">
        <strong>Description:</strong> {skillDescription}
      </div>
      <div className="text-sm mt-2">
        <strong>Stats:</strong> {skillStats}
      </div>
    </HoverCardContent>
  </HoverCard>
)

SkillButton = withClickable(SkillButton)

export { SkillButton }
