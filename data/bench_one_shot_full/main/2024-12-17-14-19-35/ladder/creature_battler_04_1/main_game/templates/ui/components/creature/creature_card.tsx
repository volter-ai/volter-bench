import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <ShadcnCard ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
        <ShadcnCardHeader uid={`${uid}-header`}>
          <ShadcnCardTitle uid={`${uid}-title`}>{name}</ShadcnCardTitle>
        </ShadcnCardHeader>
        <ShadcnCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <ShadcnProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </ShadcnCardContent>
      </ShadcnCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
