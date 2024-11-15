import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadCard, 
  CardContent as ShadCardContent, 
  CardHeader as ShadCardHeader, 
  CardTitle as ShadCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <ShadCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <ShadCardHeader uid={`${uid}-header`}>
          <ShadCardTitle uid={`${uid}-title`}>{name}</ShadCardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </ShadCardHeader>
        <ShadCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </ShadCardContent>
      </ShadCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
