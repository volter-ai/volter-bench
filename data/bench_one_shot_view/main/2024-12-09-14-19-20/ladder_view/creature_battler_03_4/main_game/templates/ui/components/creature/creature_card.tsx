import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = withClickable(BaseCard) as React.ForwardRefExoticComponent<BaseProps & React.HTMLAttributes<HTMLDivElement>>
let CardContent = withClickable(BaseCardContent) as React.ForwardRefExoticComponent<BaseProps & React.HTMLAttributes<HTMLDivElement>>
let CardHeader = withClickable(BaseCardHeader) as React.ForwardRefExoticComponent<BaseProps & React.HTMLAttributes<HTMLDivElement>>
let CardTitle = withClickable(BaseCardTitle) as React.ForwardRefExoticComponent<BaseProps & React.HTMLAttributes<HTMLHeadingElement>>

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
      <Card ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
