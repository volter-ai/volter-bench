import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as BaseCard,
  CardContent as BaseCardContent,
  CardHeader as BaseCardHeader,
  CardTitle as BaseCardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

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
      <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <BaseCardHeader uid={uid}>
          <BaseCardTitle uid={uid}>{name}</BaseCardTitle>
        </BaseCardHeader>
        <BaseCardContent uid={uid}>
          <img 
            src={image}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <Progress 
            value={(currentHp / maxHp) * 100} 
            className="w-full"
            uid={`${uid}-progress`}
          />
          <div className="text-center mt-2">
            {currentHp} / {maxHp} HP
          </div>
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
