import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"

import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => (
  <HoverCardPrimitive.Root {...props}>
    <HoverCardPrimitive.Trigger asChild>
      <button className="px-4 py-2 bg-blue-500 text-white rounded-md">
        {skillName}
      </button>
    </HoverCardPrimitive.Trigger>
    <HoverCardPrimitive.Content className="bg-white p-2 rounded-md shadow-lg">
      <div>
        <strong>Description:</strong> {skillDescription}
      </div>
      <div>
        <strong>Stats:</strong> {skillStats}
      </div>
    </HoverCardPrimitive.Content>
  </HoverCardPrimitive.Root>
)

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
