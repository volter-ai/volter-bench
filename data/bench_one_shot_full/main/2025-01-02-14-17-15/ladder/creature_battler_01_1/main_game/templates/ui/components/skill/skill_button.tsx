import * as React from "react"
import { Button, ButtonProps } from "@/components/ui/button"
import { withClickable } from '@/lib/withClickable'

interface SkillButtonProps extends ButtonProps {
  uid: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, ...props }, ref) => {
    return <Button ref={ref} {...props} />
  }
)
SkillButton.displayName = "SkillButton"
SkillButton = withClickable(SkillButton)

export { SkillButton }
